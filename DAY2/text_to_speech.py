from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENROUTER_API_KEY') # sesuaikan
)
text = "ptimasi adalah proses menemukan solusi terbaik (optimal) dari semua kemungkinan solusi yang ada untuk suatu masalah."

audio_file = Path('audio_output1.mp3')

with client.audio.speech.with_streaming_response.create(
    model='gpt-4o-mini-tts',
    voice='alloy',
    input=text
) as response:
    response.stream_to_file(audio_file)