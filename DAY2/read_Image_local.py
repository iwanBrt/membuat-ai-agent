from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPEN_AI_API')
)

def decode_image(image_path):
    with open(image_path, 'rb') as file:
        return base64.b64encode(file.read()).decode()

image_url = 'asets/ayam.jpg'

base64_image = decode_image(image_url)

response = client.chat.completions.create(
    model = 'gpt-4o',
    messages=[
        {'role' : 'user', 'content' : [
            {'type' : 'text', 'text': 'gambar apa nih?'},
            {'type' : 'image_url', 'image_url' :{'url': f'data:image/jpg;base64,{base64_image}'}},
        ]}
    ]
)
print(response.choices[0].message.content)

#print(decode_image(image_url))