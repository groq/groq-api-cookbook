import os
from groq import Groq
import requests
import json
import io
import base64
from dotenv import load_dotenv
import datetime
from moviepy import *
from moviepy.audio import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import srt

from pydub import AudioSegment
from pydub.effects import speedup

load_dotenv()  

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def convert_mp4_to_mp3(mp4_filepath, mp3_file):
    """
    Converts an MP4 file to MP3.

    Args:
        mp4_filepath: Path to the input MP4 file.
        mp3_filepath: Path to save the output MP3 file.
    """
    video_clip = VideoFileClip(mp4_filepath)

    # Extract audio from video
    video_clip.audio.write_audiofile(mp3_file)
    print("now is an mp3")
    video_clip.close()

# Step 1: Transcribe Audio
def transcribe_audio(mp3_file):

# Open the audio file
    with open(mp3_file, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(mp3_file, file.read()), # Required audio file
            model="whisper-large-v3-turbo", # Required model to use for transcription
            response_format="verbose_json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        # Print the transcription text
        print(transcription.segments)
        return transcription.segments

# takes english text into arabic
def translate(text):
    completion = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "Translate this English text into arabic. Only return the arabic response."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": f"Translate this into arabic: {text}",
        }
    ],
    max_completion_tokens=1024,
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content 

# would iterate through each timestamp and only pass in 
def convert_text_into_audio(text, index):
    url = "https://api.groq.com/openai/v1/audio/speech"
    
    headers = {
        "Authorization": f"Bearer {os.environ.get("GROQ_API_KEY")}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "playai-tts-arabic",
        "input": text,
        "voice": "Nasser-PlayAI",  # Change as needed
        "response_format": "wav"  # Explicitly set response format to WAV
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(response)
        if response.status_code == 200:
            filename = f"output_{index}.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Audio saved as {filename}")
            return
        else:
            print("here")
            return None
    except Exception as e:
        print("exception"+ e)
        return None


video_file = "input.mp4"
mp3_file = "../output.mp3"
output_file = "final_output_with_dub.mp4"

# take in video file, remove audio and get mp3 from it
convert_mp4_to_mp3(video_file, mp3_file)

# with mp3, transcribe with whisper and get sentence timestamps
segments = transcribe_audio(mp3_file)

og_subs = []
translated_subs = []
# loop through segments and translate into language then make tts call for each. also make a srt file.
for index, segment in enumerate(segments):
    english_sentence = segment["text"]

    # translate
    arabic_translated = translate(english_sentence)

    # make audio. # can make the function async in the future so it's faster since they're all going to get saved in a folder
    convert_text_into_audio(arabic_translated, index)

    start = datetime.timedelta(seconds=segment["start"])
    end = datetime.timedelta(seconds=segment["end"])
    og_subs.append(srt.Subtitle(index=segment["id"], start=start, end=end, content=segment["text"]))
    translated_subs.append(srt.Subtitle(index=segment["id"], start=start, end=end, content=arabic_translated))
    print(start, end, "\n")

# Make an (translated).srt file from the whisper time stamps
srt_file1 = "../subtitles.srt"
srt_file2 = "../translated_subtitles.srt"
with open(srt_file1, "w", encoding="utf-8") as f:
    f.write(srt.compose(og_subs))

with open(srt_file2, "w", encoding="utf-8") as f:
    f.write(srt.compose(translated_subs))

def adjust_audio_speed(audio, max_duration_ms):
    """Adjust audio speed to fit within max_duration_ms in one step."""
    current_length = len(audio)
    if current_length <= max_duration_ms:
        return audio
    
    # Calculate required speed factor directly
    required_speed_factor = current_length / max_duration_ms
    return speedup(audio, playback_speed=required_speed_factor)

# once all audio are complete, merge them together.
def process_audio_segments(segments, output_filename="final_output.wav"):
    # First, determine the total duration needed
    max_end_time_ms = 0
    for segment in segments:
        end_ms = int(float(segment["end"]) * 1000)
        if end_ms > max_end_time_ms:
            max_end_time_ms = end_ms
    
    # Create an empty audio segment for the entire duration
    final_audio = AudioSegment.silent(duration=max_end_time_ms + 1000)  # Add some buffer
    
    # Place each segment at its correct position
    for index, segment in enumerate(segments):
        start_ms = int(float(segment["start"]) * 1000)
        end_ms = int(float(segment["end"]) * 1000)
        max_duration_ms = end_ms - start_ms  # Allowed duration
        
        print(f"Segment {index}: Start: {start_ms} ms, End: {end_ms} ms, Max Duration: {max_duration_ms} ms")
        
        # Load corresponding audio file
        file_name = f"output_{index}.wav"
        if not os.path.exists(file_name):
            print(f"File {file_name} not found, skipping...")
            continue
        
        # Load the audio
        audio = AudioSegment.from_wav(file_name)
        print(f"Original audio length: {len(audio)} ms")
        
        # Adjust speed if too long (using improved function)
        if len(audio) > max_duration_ms:
            audio = adjust_audio_speed(audio, max_duration_ms)
            print(f"Adjusted audio length: {len(audio)} ms")
        
        # Overlay at the correct position
        final_audio = final_audio.overlay(audio, position=start_ms)
    
    # Export the final merged audio with specific parameters
    final_audio.export(
        output_filename, 
        format="wav",
        parameters=["-ar", "44100", "-ac", "1", "-ab", "192k"]  # Consistent export parameters
    )
    print(f"Final audio saved as {output_filename}")
    
process_audio_segments(segments)


def replace_audio(mp4_file, wav_file, output_file="output_video.mp4"):
    # Load the video file (without audio)
    video = VideoFileClip(mp4_file).without_audio()

    # Load the new audio file
    new_audio = AudioFileClip(wav_file)

    # With new audio to the video
    final_video = video.with_audio(new_audio)

    # Export the final video with new audio
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

    print(f"New video saved as {output_file}")

# Example usage
replace_audio(video_file, "final_output.wav", "final.mp4")

# you could do them async to make the audio generation part faster