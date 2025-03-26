import streamlit as st
import tempfile
import os
import datetime
from groq import Groq
from io import BytesIO
from dotenv import load_dotenv
from collections import defaultdict
from moviepy.video.io.VideoFileClip import VideoFileClip


load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", None)
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

st.set_page_config(page_title="Video Transcription & Analysis", layout="centered")

if 'api_key' not in st.session_state:
    st.session_state.api_key = GROQ_API_KEY


# Initialize Groq client only once
if 'groq' not in st.session_state or st.session_state.groq is None:
    if GROQ_API_KEY:
        st.session_state.groq = client
    else:
        st.session_state.groq = None  # Ensure it's explicitly set to None if no key

def convert_mp4_to_mp3(mp4_filepath, mp3_filepath):
    video_clip = VideoFileClip(mp4_filepath)
    video_clip.audio.write_audiofile(mp3_filepath)
    print(mp3_filepath + "\n")
    video_clip.close()

def transcribe_audio(mp3_filepath):
    if 'groq' not in st.session_state or st.session_state.groq is None:
        st.error("Groq client is not initialized. Please check your API Key.")
        st.stop()
    
    # check which models are available
    # print(st.session_state.groq.models.list())
    
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
    """Send top words to Groq for analysis and return the summary"""
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


st.title("Upload a Video for Transcription")

with st.form("groqform"):
    if not GROQ_API_KEY:
        st.session_state.api_key = st.text_input("Enter your Groq API Key (gsk_yA...):", "", type="password", autocomplete="off")
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if not st.session_state.api_key and not GROQ_API_KEY:
            st.sidebar.warning("Invalid API Key!")
            st.stop()

        # Debugging: Log API key usage
        # st.write("Using API Key:", st.session_state.api_key if st.session_state.api_key else GROQ_API_KEY)

        st.session_state.groq = Groq(api_key=st.session_state.api_key if st.session_state.api_key else GROQ_API_KEY)

    video_path = None
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            tmp_video.write(uploaded_file.read())
            video_path = tmp_video.name
        
        # side = 80
        # width = 200
        # _, container, _ = st.columns([side, width, side])
        # if video_path:
        #     container.video(video_path)

       
        mp3_path = video_path.replace(".mp4", ".mp3")
        convert_mp4_to_mp3(video_path, mp3_path)
        
        st.write("Transcription in Progress...")
        transcription_data = transcribe_audio(mp3_path)
        
        if transcription_data:
            st.success("Transcription Completed!")
            word_map = defaultdict(list)
            word_count = defaultdict(int)

            for segment in transcription_data:
                word = segment["word"].lower().replace(".", "").replace("?", "").replace("!", "").replace(",", "")
                start_seconds = segment["start"]  # Keep as float
                start_time = str(datetime.timedelta(seconds=start_seconds))  # Convert to HH:MM:SS format
                word_map[word].append((start_seconds, start_time))  # Store both float and formatted time
                word_count[word] += 1
            
            # Filter out common stop words and get top 20 words
            sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            top_20_words = sorted_words[:20]  # Get only top 20 words

            st.subheader("Top 20 Words")
            # Create two columns
            col1, col2 = st.columns(2)

            # Split the words between the two columns
            for i, (word, count) in enumerate(top_20_words):
                if i % 2 == 0:
                    col1.write(f"**{word}**: {count} times")
                else:
                    col2.write(f"**{word}**: {count} times")
            
            # Get analysis of top words
            with st.spinner("Analyzing top words..."):
                st.subheader("Content Analysis")
                analysis = get_top_words_analysis(top_20_words)
                st.write(analysis)
            
            st.subheader("Search for a Word")
            search_word = st.text_input("Enter a word to see when it's mentioned", autocomplete=None).lower()
            
            # Display video
            st.video(video_path)
            
            # Search functionality with clickable timestamps
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

            st.subheader("Frequency of All Words")

           # Create a defaultdict to group words by their counts
            word_groups = defaultdict(list)

            # Group words by their count
            for word, count in sorted_words:
                word_groups[count].append(word)

            # Now display the count and the array of words that have that count
            for count, words in sorted(word_groups.items(), reverse=True):
                st.write(f"**{count} times**: {', '.join(words)}")
            
            

        os.remove(video_path)
        os.remove(mp3_path)
