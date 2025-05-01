# Groq Translation Dubbing

This code uses Groq's LLM, Speech-To-Text, and PlayAI Text-To-Speech (hosted on Groq) to translate videos by transcribing, translating, and dubbing content with new audio in a different language.

Written by: Chris Ho

## Setup

Clone the repository and navigate to the main folder:

`cd translation-dubbing`

Create and activate a virtual environment:

`python3 -m venv venv`

`source venv/bin/activate`

Install required dependencies:

`pip3 install groq moviepy srt requests python-dotenv pydub`

Create a .env file with your Groq API key:

`GROQ_API_KEY=your_groq_api_key_here`

### How to Run

Place your video file as `input.mp4` in the parent directory
Run the script:

`python3 dubbing.py`

The final dubbed video will be saved as `final.mp4`

# How it works
- The script extracts the audio from the input video file
- It transcribes the audio using Groq's Whisper model
- Each text segment is translated from English to Arabic
- The translated text is converted to speech using Groq's TTS API
- Audio segments are adjusted for timing and combined
- Finally, the original video is combined with the new audio track

## 1. Converting MP4 to MP3
```
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
```

## 2. Transcribing Audio
```
def transcribe_audio(mp3_file):
    # Open the audio file
    with open(mp3_file, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(mp3_file, file.read()), # Required audio file
            model="whisper-large-v3-turbo", # Required model for transcription
            response_format="verbose_json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        # Print the transcription text
        print(transcription.segments)
        return transcription.segments
```

## 3. Translating Text
```
def translate(text):
    completion = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
        {
            "role": "system",
            "content": "Translate this English text into arabic. Only return the arabic response."
        },
        {
            "role": "user",
            "content": f"Translate this into arabic: {text}",
        }
    ],
    max_completion_tokens=1024,
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
```
## 4. Converting Text to Audio
```
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
```
## 5. Adjusting Audio Speed
```
def adjust_audio_speed(audio, max_duration_ms):
    """Adjust audio speed to fit within max_duration_ms in one step."""
    current_length = len(audio)
    if current_length <= max_duration_ms:
        return audio
    
    # Calculate required speed factor directly
    required_speed_factor = current_length / max_duration_ms
    return speedup(audio, playback_speed=required_speed_factor)
```
## 6. Processing Audio Segments
```
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
        
        # Load corresponding audio file
        file_name = f"output_{index}.wav"
        if not os.path.exists(file_name):
            print(f"File {file_name} not found, skipping...")
            continue
        
        # Load the audio
        audio = AudioSegment.from_wav(file_name)
        
        # Adjust speed if too long
        if len(audio) > max_duration_ms:
            audio = adjust_audio_speed(audio, max_duration_ms)
        
        # Overlay at the correct position
        final_audio = final_audio.overlay(audio, position=start_ms)
    
    # Export the final merged audio
    final_audio.export(
        output_filename, 
        format="wav",
        parameters=["-ar", "44100", "-ac", "1", "-ab", "192k"]
    )
```
## 7. Replacing Audio in Video
```
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
```


### Output Files

- output.mp3: Extracted audio from the original video
- subtitles.srt: Original language subtitles
- translated_subtitles.srt: Translated subtitles
- output_[index].wav: Individual audio segments for each translated line
- final_output.wav: Combined audio track
- final.mp4: Final video with translated audio