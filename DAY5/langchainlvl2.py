from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
# perlu sistem prompt untuk chat model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


#messges

#prompt template
SYSTEM_PROMPT = 'You are a helpful assistant'

prompt = ChatPromptTemplate.from_messages([
    ('system', SYSTEM_PROMPT),
    MessagesPlaceholder('chat_history'),
    ('human', '{input}')
])

#history messeges

llm = ChatOpenAI(
    model='gpt-4o-mini',
)

chain = prompt | llm 


sesion_store = {}
def get_history(sesion_id):
    if sesion_id not in sesion_store:
        sesion_store[sesion_id] = InMemoryChatMessageHistory()
    return sesion_store[sesion_id]


agent = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key='input',
    history_messages_key='chat_history'
    
)

#chat looping
session_id = 'demo-level-2'
while True:
    user_text = input('\nYou:  ').strip()
    
    # gunakan `agent` (RunnableWithMessageHistory) agar `chat_history` disuntikkan
    ai_message = agent.invoke({'input': user_text},
                              config={'configurable': {
                                  'session_id': session_id}})
    print(f'AI: {ai_message.content}')