#memasukkan gambar dari url online
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

image_url = "https://tse1.mm.bing.net/th/id/OIP.tizfvtzn8aUsS3WvduVmdgHaLG?pid=Api&P=0&h=180"

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {'role':'user', 'content':[
            {'type':'text', 'text':'siapa dia?'},
            {"type":"image_url", "image_url":{"url":image_url}},
        ]}
    ]
)

print(response.choices[0].message.content)