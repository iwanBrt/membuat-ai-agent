from openai import OpenAI
from dotenv import load_dotenv#mengimport smua api key dari env
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

try:
    models = client.models.list()
    print("sukses")
    print(f'ALL models: {models.data}')
except Exception as e:
    pass