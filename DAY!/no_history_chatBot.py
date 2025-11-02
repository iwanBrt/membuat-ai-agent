from openai import OpenAI
from dotenv import load_dotenv #mengimport smua api key dari env
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = "You are a helpful assistant."
MAX_HISTORY = 12 * 2 + 1  # 12 user-assistant pairs + system prompt

history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_chat = input('You: ')
    
    if user_chat == '/exit':
        break
    
    history.append({"role": "user", "content": user_chat})

# client.chat.completions.create()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )


    history.append({"role": "assistant", "content": response.choices[0].message.content})
    
    if len(history) > MAX_HISTORY:
        #summarize history or trim
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )
        
        new_history = [history[0]] # keep system prompt
        history = new_history
        
        
    print(f"AI: {response.choices[0].message.content}")