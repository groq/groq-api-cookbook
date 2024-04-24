import dotenv
import os
import requests
import pydub
from pydub import AudioSegment
from pydub.playback import play
import logging

dotenv.load_dotenv()

class VoiceTools:
    def __init__(self):
        self.agent_voices = {
            "Annie": "aura-luna-en",
            "Mike": "aura-angus-en",
            "Bob": "aura-zeus-en",
            "Alex": "aura-orpheus-en"
        }

    def text_to_speech(self, text, agent_name):
        voice_model = self.agent_voices.get(agent_name, "aura-luna-en")  # Default to Annie's voice if agent not found
        url = f"https://api.deepgram.com/v1/speak?model={voice_model}"
        api_key = os.getenv("DEEPGRAM_API_KEY")
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }

        if len(text) > 2000:
            text = text[:2000]  # Truncate the text to 2000 characters
            logging.warning(f"Input text for {agent_name} exceeded the maximum character limit. Truncating to 2000 characters.")

        payload = {"text": text}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            output_file_path = f"{agent_name.lower()}_output.mp3"
            with open(output_file_path, "wb") as f:
                f.write(response.content)

            # Convert to WAV for direct playback
            audio = AudioSegment.from_file(output_file_path)
            play(audio)  # Play the audio directly without using external programs
            
            print(f"{agent_name}'s speech saved and playing successfully.")
        else:
            print(f"Error generating speech for {agent_name}: {response.status_code} - {response.text}")