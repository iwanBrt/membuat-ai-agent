from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

text = "aku baik hati"

#client.embeddings.create
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

embedding_data = response.data[0].embedding

print(f'Text: {text}')
print(f'DImension of embedding: {len(embedding_data)}')
print(f'Embedding firts 10 values: {embedding_data[:10]}')