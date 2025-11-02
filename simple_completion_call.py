from openai import OpenAI
from dotenv import load_dotenv #mengimport smua api key dari env
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

history = []

while True:
    user_chat = input("You: ")
    
    if user_chat =='/exit':
        break

# client.chat.completions.create()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_chat},
        ]
    )

print(f"AI:{response.choices[0].message.content}")