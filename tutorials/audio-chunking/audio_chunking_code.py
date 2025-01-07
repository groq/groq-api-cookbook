from groq import Groq, RateLimitError
from pydub import AudioSegment
import json
from pathlib import Path
from datetime import datetime
import time
import subprocess
import os
import tempfile
import re

def preprocess_audio(input_path: Path) -> Path:
    """
    Preprocess audio file to 16kHz mono FLAC using ffmpeg.
    FLAC provides lossless compression for faster upload times.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with tempfile.NamedTemporaryFile(suffix='.flac', delete=False) as temp_file:
        output_path = Path(temp_file.name)
        
    print("Converting audio to 16kHz mono FLAC...")
    try:
        subprocess.run([
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error',
            '-i', input_path,
            '-ar', '16000',
            '-ac', '1',
            '-c:a', 'flac',
            '-y',
            output_path
        ], check=True) 
        return output_path
    # We'll raise an error if our FFmpeg conversion fails
    except subprocess.CalledProcessError as e:
        output_path.unlink(missing_ok=True)
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr}")
    
def transcribe_single_chunk(client: Groq, chunk: AudioSegment, chunk_num: int, total_chunks: int) -> tuple[dict, float]:
    """
    Transcribe a single audio chunk with Groq API.
    
    Args:
        client: Groq client instance
        chunk: Audio segment to transcribe
        chunk_num: Current chunk number
        total_chunks: Total number of chunks
        
    Returns:
        Tuple of (transcription result, processing time)

    Raises:
        Exception: If chunk transcription fails after retries
    """
    total_api_time = 0
    
    while True:
        with tempfile.NamedTemporaryFile(suffix='.flac') as temp_file:
            chunk.export(temp_file.name, format='flac')
            
            start_time = time.time()
            try:
                result = client.audio.transcriptions.create(
                    file=("chunk.flac", temp_file, "audio/flac"),
                    model="whisper-large-v3",
                    language="en", # We highly recommend specifying the language of your audio if you know it
                    response_format="verbose_json"
                )
                api_time = time.time() - start_time
                total_api_time += api_time
                
                print(f"Chunk {chunk_num}/{total_chunks} processed in {api_time:.2f}s")
                return result, total_api_time
                
            except RateLimitError as e:
                print(f"\nRate limit hit for chunk {chunk_num} - retrying in 60 seconds...")
                time.sleep(60)  # default wait time
                continue
                
            except Exception as e:
                print(f"Error transcribing chunk {chunk_num}: {str(e)}")
                raise

def find_longest_common_sequence(sequences: list[str], match_by_words: bool = True) -> str:
    """
    Find the optimal alignment between sequences with longest common sequence and sliding window matching.
    
    Args:
        sequences: List of text sequences to align and merge
        match_by_words: Whether to match by words (True) or characters (False)
        
    Returns:
        str: Merged sequence with optimal alignment
        
    Raises:
        RuntimeError: If there's a mismatch in sequence lengths during comparison
    """
    if not sequences:
        return ""

    # Convert input based on matching strategy
    if match_by_words:
        sequences = [
            [word for word in re.split(r'(\s+\w+)', seq) if word]
            for seq in sequences
        ]
    else:
        sequences = [list(seq) for seq in sequences]

    left_sequence = sequences[0]
    left_length = len(left_sequence)
    total_sequence = []

    for right_sequence in sequences[1:]:
        max_matching = 0.0
        right_length = len(right_sequence)
        max_indices = (left_length, left_length, 0, 0)

        # Try different alignments
        for i in range(1, left_length + right_length + 1):
            # Add epsilon to favor longer matches
            eps = float(i) / 10000.0

            left_start = max(0, left_length - i)
            left_stop = min(left_length, left_length + right_length - i)
            left = left_sequence[left_start:left_stop]

            right_start = max(0, i - left_length)
            right_stop = min(right_length, i)
            right = right_sequence[right_start:right_stop]

            if len(left) != len(right):
                raise RuntimeError(
                    "Mismatched subsequences detected during transcript merging."
                )

            matches = sum(a == b for a, b in zip(left, right))
            
            # Normalize matches by position and add epsilon 
            matching = matches / float(i) + eps

            # Require at least 2 matches
            if matches > 1 and matching > max_matching:
                max_matching = matching
                max_indices = (left_start, left_stop, right_start, right_stop)

        # Use the best alignment found
        left_start, left_stop, right_start, right_stop = max_indices
        
        # Take left half from left sequence and right half from right sequence
        left_mid = (left_stop + left_start) // 2
        right_mid = (right_stop + right_start) // 2
        
        total_sequence.extend(left_sequence[:left_mid])
        left_sequence = right_sequence[right_mid:]
        left_length = len(left_sequence)

    # Add remaining sequence
    total_sequence.extend(left_sequence)
    
    # Join back into text
    if match_by_words:
        return ''.join(total_sequence)
    return ''.join(total_sequence)

def merge_transcripts(results: list[tuple[dict, int]]) -> dict:
    """
    Merge transcription chunks and handle overlaps by:
    1. Merge all segments within each chunk's overlap/stride
    2. Merge chunk boundaries using find_longest_common_sequence
    
    Args:
        results: List of (result, start_time) tuples
        
    Returns:
        dict: Merged transcription
    """
    print("\nMerging results...")
    final_segments = []
    
    # Process each chunk's segments
    processed_chunks = []
    for i, (chunk, _) in enumerate(results):
        # Extract full segment data including metadata
        data = chunk.model_dump() if hasattr(chunk, 'model_dump') else chunk
        segments = data['segments']
        
        # If not last chunk, find next chunk start time
        if i < len(results) - 1:
            next_start = results[i + 1][1]
            
            # Split segments into current and overlap based on next chunk's start time
            current_segments = []
            overlap_segments = []
            
            for segment in segments:
                if segment['end'] * 1000 > next_start:
                    overlap_segments.append(segment)
                else:
                    current_segments.append(segment)
            
            # Merge overlap segments if any exist
            if overlap_segments:
                merged_overlap = overlap_segments[0].copy()
                merged_overlap.update({
                    'text': ' '.join(s['text'] for s in overlap_segments),
                    'end': overlap_segments[-1]['end']
                })
                current_segments.append(merged_overlap)
                
            processed_chunks.append(current_segments)
        else:
            # For last chunk, keep all segments
            processed_chunks.append(segments)
    
    # Merge boundaries between chunks
    for i in range(len(processed_chunks) - 1):
        # Add all segments except last from current chunk
        final_segments.extend(processed_chunks[i][:-1])
        
        # Merge boundary segments
        last_segment = processed_chunks[i][-1]
        first_segment = processed_chunks[i + 1][0]
        
        merged_text = find_longest_common_sequence([last_segment['text'], first_segment['text']])
        merged_segment = last_segment.copy()
        merged_segment.update({
            'text': merged_text,
            'end': first_segment['end']
        })
        final_segments.append(merged_segment)
    
    # Add all segments from last chunk
    if processed_chunks:
        final_segments.extend(processed_chunks[-1])
    
    # Create final transcription
    final_text = ' '.join(segment['text'] for segment in final_segments)
    
    return {
        "text": final_text,
        "segments": final_segments
    }

def save_results(result: dict, audio_path: Path) -> Path:
    """
    Save transcription results to files.
    
    Args:
        result: Transcription result dictionary
        audio_path: Original audio file path
        
    Returns:
        base_path: Base path where files were saved

    Raises:
        IOError: If saving results fails
    """
    try:
        output_dir = Path("transcriptions")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_path = output_dir / f"{Path(audio_path).stem}_{timestamp}"
        
        # Save results in different formats
        with open(f"{base_path}.txt", 'w', encoding='utf-8') as f:
            f.write(result["text"])
        
        with open(f"{base_path}_full.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        with open(f"{base_path}_segments.json", 'w', encoding='utf-8') as f:
            json.dump(result["segments"], f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to transcriptions folder:")
        print(f"- {base_path}.txt")
        print(f"- {base_path}_full.json")
        print(f"- {base_path}_segments.json")
        
        return base_path
    
    except IOError as e:
        print(f"Error saving results: {str(e)}")
        raise

def transcribe_audio_in_chunks(audio_path: Path, chunk_length: int = 600, overlap: int = 10) -> dict:
    """
    Transcribe audio in chunks with overlap with Whisper via Groq API.
    
    Args:
        audio_path: Path to audio file
        chunk_length: Length of each chunk in seconds
        overlap: Overlap between chunks in seconds
    
    Returns:
        dict: Containing transcription results
    
    Raises:
        ValueError: If Groq API key is not set
        RuntimeError: If audio file fails to load
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    print(f"\nStarting transcription of: {audio_path}")
    # Make sure your Groq API key is configured. If you don't have one, you can get one at https://console.groq.com/keys!
    client = Groq(api_key=api_key, max_retries=0)
    
    processed_path = None
    try:
        # Preprocess audio and get basic info
        processed_path = preprocess_audio(audio_path)
        try:
            audio = AudioSegment.from_file(processed_path, format="flac")
        except Exception as e:
            raise RuntimeError(f"Failed to load audio: {str(e)}")
        
        duration = len(audio)
        print(f"Audio duration: {duration/1000:.2f}s")
        
        # Calculate # of chunks
        chunk_ms = chunk_length * 1000
        overlap_ms = overlap * 1000
        total_chunks = (duration // (chunk_ms - overlap_ms)) + 1
        print(f"Processing {total_chunks} chunks...")
        
        results = []
        total_transcription_time = 0

        # Loop through each chunk, extract current chunk from audio, transcribe    
        for i in range(total_chunks):
            start = i * (chunk_ms - overlap_ms)
            end = min(start + chunk_ms, duration)
                
            print(f"\nProcessing chunk {i+1}/{total_chunks}")
            print(f"Time range: {start/1000:.1f}s - {end/1000:.1f}s")
                
            chunk = audio[start:end]
            result, chunk_time = transcribe_single_chunk(client, chunk, i+1, total_chunks)
            total_transcription_time += chunk_time
            results.append((result, start))
            
        final_result = merge_transcripts(results)
        save_results(final_result, audio_path)
            
        print(f"\nTotal Groq API transcription time: {total_transcription_time:.2f}s")
        
        return final_result
    
    # Clean up temp files regardless of successful creation    
    finally:
        if processed_path:
            Path(processed_path).unlink(missing_ok=True)

if __name__ == "__main__":
    transcribe_audio_in_chunks(Path("path_to_your_audio"))