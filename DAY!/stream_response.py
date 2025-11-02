from openai import OpenAI
from dotenv import load_dotenv #mengimport smua api key dari env
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# client.chat.completions.create()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "halo, apa kabar? jelaskan tentang quantum computing secara singkat."}
    ],
    stream=True,#defaultnya false(response full), kalo true streaming
    
)

full_response = ""

#chunk.choices[0].delta.content
for chunk in response:#responsenya berupa generator
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end='', flush=True)#flush biar langsung ke print
        full_response += content
#print(response.choices[0].message.content)