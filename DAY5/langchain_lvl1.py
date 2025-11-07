from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# perlu sistem prompt untuk chat model
from langchain_core.prompts import ChatPromptTemplate

#messges

#prompt template
SYSTEM_PROMPT = """You are a helpful assistant  ."""

prompt = ChatPromptTemplate([
    ('system', SYSTEM_PROMPT),
    ('Human', '{input}')
])

#history messeges

llm = ChatOpenAI(
    model='gpt-4o-mini',
)

chain = prompt | llm 

#chat looping
while True:
    user_text = input('\nYou:  ').strip()
    
    ai_messege = chain.invoke({'input':user_text})
    print(f'AI: {ai_messege.content}')