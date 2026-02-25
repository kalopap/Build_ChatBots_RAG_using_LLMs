import config
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

## Initialize the llm
llm1 = ChatOllama(
    model="qwen2.5:latest",
    base_url="http://localhost:11434"
)

#### Creating prompts 
system_prompt = "You are a financial expert specialized in analysis Indian demat account statements and transactions. Always Follow the instructions strictly!"
prompt1 = "What type of 2 useful reports or data can you generate if I share my past financial year's demat account statement?"

followup1 = "Do you already know the formulas needed for these reports? Don't share the formulas. "

followup2 = "Can you calculate whether a sale comes under Long Term or Short Term Capital gains? Just say yes or no"


### Create Chat Template
prompt_template1 = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    ('placeholder',"{history_key}"),
    ("user","{prompt_key}")
])

## Chaining
chain1 = prompt_template1 | llm1 | StrOutputParser()

### Creating a session

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

#### Creating history of the conversation

fin_history = RunnableWithMessageHistory(
    chain1,
    get_session_history,
    input_messages_key="prompt_key",
    history_messages_key="history_key"
)

session_id_k = "Kalyani"

get_session_history(session_id_k).clear()

response1 = fin_history.invoke(
    {"prompt_key":prompt1},
    config={"configurable":{"session_id":session_id_k}}
)
print(response1)
print("---------------Answer to the follow-up question-----------")

##Follow up 1
response2 = fin_history.invoke(
    {"prompt_key":followup1},
    config={"configurable":{"session_id":session_id_k}}
)
print(response2)
print("---------------Answer to the follow-up question 2----------")

### Follow up 2
response3 = fin_history.invoke(
    {"prompt_key":followup2},
    config={"configurable":{"session_id":session_id_k}}
)
print(response3)