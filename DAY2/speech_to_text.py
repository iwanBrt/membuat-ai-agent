from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPEN_AI_API')
)

audio_path = 'audio_dummy.mp3'

with open(audio_path, 'rb') as audio_file:
    result = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio_file,
        response_format='text'
    )
    
print(f'hasil transkripsi:\n, {result}')