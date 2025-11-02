#memasukkan gambar dari url online
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

#improve promt
prompt = "buat gambar pemandangan di hari yang cerah dengan gunung dan danau di depannya, dengan gaya lukisan cat minyak"

response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    n=1,#jumlah gambar
    size="1024x1024",
    quality="standard"
    
)

#melhat url
image_url = response.data[0].url
print(f'URL: {image_url}')

image_data = requests.get(image_url).content
file_name = f'gambar_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
with open(file_name, 'wb') as f:
    f.write(image_data)