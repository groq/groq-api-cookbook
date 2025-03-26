# video-word-search

https://github.com/user-attachments/assets/b9cb07aa-e82a-474f-bdba-03ae92be9f22

Created by: Chris Ho

This Streamlit application lets users upload a video file and get timestamps for each word spoken (with the ability to jump to each timestamp by clicking on it), the frequency of each word used, as well as analysis based on the top 20 words used.



## Part 1: Imports and Initial Setup

- Sign up for a free Groq API key [here.](https://console.groq.com/)
- Import necessary libraries
- Set up environment variables
- Configure Streamlit page and session state

```
# Part 1: Imports and Initial Setup
import streamlit as st
import tempfile
import os
import datetime
from groq import Groq
from io import BytesIO
from dotenv import load_dotenv
from collections import defaultdict
from moviepy.video.io.VideoFileClip import VideoFileClip

# Load environment variables
load_dotenv()

# API Key and Client Setup
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", None)
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Streamlit Page Configuration
st.set_page_config(page_title="Video Transcription & Analysis", layout="centered")

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = GROQ_API_KEY
```


## Part 2: Helper Functions

`convert_mp4_to_mp3()`: Converts video to audio
`transcribe_audio()`: Transcribes audio using Groq Whisper
`get_top_words_analysis()`: Analyzes top words using your choice of LLM hosted on Groq
```
# Part 2: Helper Functions for Video Processing and Transcription
def convert_mp4_to_mp3(mp4_filepath, mp3_filepath):
    """Convert video file to audio file"""
    video_clip = VideoFileClip(mp4_filepath)
    video_clip.audio.write_audiofile(mp3_filepath)
    print(mp3_filepath + "\n")
    video_clip.close()

def transcribe_audio(mp3_filepath):
    """Transcribe audio using Groq Whisper"""
    if 'groq' not in st.session_state or st.session_state.groq is None:
        st.error("Groq client is not initialized. Please check your API Key.")
        st.stop()
    
    try:
        with open(mp3_filepath, "rb") as audio_file:
            transcription = st.session_state.groq.audio.transcriptions.create(
                file=(mp3_filepath, audio_file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
                timestamp_granularities=["word"],
                language="en"
            )
        print(transcription)
        return transcription.words
    except Exception as e:
        st.error(f"Transcription error: {e}")
        return None

def get_top_words_analysis(top_words):
    """Analyze top words using Groq Chat Completion"""
    if 'groq' not in st.session_state or st.session_state.groq is None:
        st.error("Groq client is not initialized. Please check your API Key.")
        return "Unable to analyze: Groq client not initialized."
    
    # Format the top words into a string
    words_str = ", ".join([f"{word} ({count})" for word, count in top_words])
    
    prompt = f"""
    Here are the 20 top words from a video transcription:
    {words_str}
    
    You are a speech and presentation coach. Based on these words, analyze how an audience might feel or react to these words. Provide helpful feedback on word choices.
    """

    try:
        chat_completion = st.session_state.groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes video transcription data."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_completion_tokens=5012,
            top_p=1,
            stream=False
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error analyzing top words: {str(e)}"

```


## Part 3: Main Streamlit Application Logic

- Create form for API key and file upload
- Handle video processing
- Perform transcription
- Display word analysis
- Provide interactive word search
- Clean up temporary files
```
# Part 3: Main Streamlit Application Logic
st.title("Upload a Video for Transcription")

with st.form("groqform"):
    # API Key Input (if not preset)
    if not GROQ_API_KEY:
        st.session_state.api_key = st.text_input("Enter your Groq API Key (gsk_yA...):", "", type="password", autocomplete="off")
    
    # File Uploader
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Validate API Key
        if not st.session_state.api_key and not GROQ_API_KEY:
            st.sidebar.warning("Invalid API Key!")
            st.stop()

        # Initialize Groq Client
        st.session_state.groq = Groq(api_key=st.session_state.api_key if st.session_state.api_key else GROQ_API_KEY)

        video_path = None
        if uploaded_file:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
                tmp_video.write(uploaded_file.read())
                video_path = tmp_video.name
            
            # Convert video to audio
            mp3_path = video_path.replace(".mp4", ".mp3")
            convert_mp4_to_mp3(video_path, mp3_path)
            
            st.write("Transcription in Progress...")
            transcription_data = transcribe_audio(mp3_path)
            
            if transcription_data:
                st.success("Transcription Completed!")
                
                # Process transcription data
                word_map = defaultdict(list)
                word_count = defaultdict(int)

                for segment in transcription_data:
                    word = segment["word"].lower().replace(".", "").replace("?", "").replace("!", "").replace(",", "")
                    start_seconds = segment["start"]
                    start_time = str(datetime.timedelta(seconds=start_seconds))
                    word_map[word].append((start_seconds, start_time))
                    word_count[word] += 1
                
                # Get top 20 words
                sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
                top_20_words = sorted_words[:20]

                # Display top words
                st.subheader("Top 20 Words")
                col1, col2 = st.columns(2)
                for i, (word, count) in enumerate(top_20_words):
                    if i % 2 == 0:
                        col1.write(f"**{word}**: {count} times")
                    else:
                        col2.write(f"**{word}**: {count} times")
                
                # Analyze top words
                with st.spinner("Analyzing top words..."):
                    st.subheader("Content Analysis")
                    analysis = get_top_words_analysis(top_20_words)
                    st.write(analysis)
                
                # Word search functionality
                st.subheader("Search for a Word")
                search_word = st.text_input("Enter a word to see when it's mentioned", autocomplete=None).lower()
                
                # Display video
                st.video(video_path)
                
                # Word occurrence search
                occurrences = word_map.get(search_word, [])
                if occurrences:
                    st.success(f"**'{search_word}'** appears **{len(occurrences)}** times at:")
                    count = 1
                    for start_seconds, timestamp in occurrences:
                        st.components.v1.html(
                            f"""
                            <script>
                                function seekVideo_{int(start_seconds*1000)}() {{
                                    var video = parent.document.querySelector('video');
                                    if (video) {{
                                        video.currentTime = {start_seconds};
                                        video.play();
                                    }}
                                }}
                            </script>

                            <div style="display: flex; align-items: center;">
                                <span style="font-size:18px; font-weight:bold; margin-right: 10px;">{count}.</span>
                                <button onclick="seekVideo_{int(start_seconds*1000)}()" 
                                    style="padding:8px 12px; background-color:#007bff; color:white; border:none; 
                                    border-radius:5px; cursor:pointer; transition: background-color 0.3s;"
                                    onmouseover="this.style.backgroundColor='#0056b3'" 
                                    onmouseout="this.style.backgroundColor='#007bff'">
                                    🕒 {timestamp}
                                </button>
                            </div>
                            """,
                            height=55,
                        )
                        count += 1
                else:
                    if search_word != "" and len(search_word) > 0:
                        st.warning(f"'{search_word}' not found in the transcript.")

                # Word frequency display
                st.subheader("Frequency of All Words")
                word_groups = defaultdict(list)

                for word, count in sorted_words:
                    word_groups[count].append(word)

                for count, words in sorted(word_groups.items(), reverse=True):
                    st.write(f"**{count} times**: {', '.join(words)}")
                
                # Clean up temporary files
                os.remove(video_path)
                os.remove(mp3_path)
```


## How to run it

Make a virtual python environment

```python3 -m venv venv```

Use the venv

`source venv/bin/activate`

Install the necessary packages

`pip3 install groq requests python-dotenv streamlit moviepy`

Run the app

`streamlit run app.py`


Fun fact: The algorithm behind the word count frequency came from [this Leetcode question.](https://leetcode.com/problems/top-k-frequent-elements/description/)
