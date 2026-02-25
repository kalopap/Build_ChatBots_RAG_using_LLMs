from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.runnables import chain
from sqlalchemy import create_engine
import streamlit as st

###Load dot env 
load = load_dotenv()

### Initialize an LLM
llm1 = ChatOllama(
    base_url="http://localhost:11434",
    model="qwen2.5:latest",
    temperature=0.2,
    max_tokens = 300
)

## Method to create session with sql chat history 
engine = create_engine("sqlite:///user_chathistory.db")

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id=session_id,connection=engine)

### Design Chatbot page with StreamLit
chat_session_id = "VamsiBot"

with st.sidebar:
    chat_session_id = st.text_input("Enter your name",chat_session_id)
    if st.button("New Chat"):
        st.session_state.prev_chat_history = []
        get_session_history(chat_session_id).clear()
    
    
st.markdown(
    """ 
        <h2 align=center>Hello, How can I help you today?</h2>
    """,
    unsafe_allow_html=True
)
    
##Clear only if it is a new session, we want the previous conversation too
if 'prev_chat_history' not in st.session_state:
    st.session_state.prev_chat_history = []

### TO keep the previous message when there is a followup
for message in st.session_state.prev_chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
### Create prompts
system_prompt = "You are an AI expert"

### Create Prompt Template
chat_prompt_template = ChatPromptTemplate([
    ("system",system_prompt),
    ("placeholder","{usr_history_key}"),
    ("user","{usr_prompt_key}")
])

## chain the steps
chain1 = chat_prompt_template | llm1 | StrOutputParser()

## Configure history Runnable(write a method)
def invoke_chat_history(chain_u,session_id_u,prompt_msg):

    user_chat_history = RunnableWithMessageHistory(
    chain_u,
    get_session_history,
    input_messages_key="usr_prompt_key",
    history_messages_key="usr_history_key")
    for response in user_chat_history.stream({"usr_prompt_key":prompt_msg},
                                             config={"configurable":{"session_id":session_id_u}}):
        yield response

    

### Invoke the prompts in UI and storing each prompts and response to the history
prompt_input1 = st.chat_input("Type Here..")
if prompt_input1:
    st.session_state.prev_chat_history.append({'role':'user', "content": prompt_input1})
    #st.write(prompt_input1)
    with st.chat_message('user'):
        st.markdown(prompt_input1)

    
    with st.chat_message('assistant'):
        ai_response1 = st.write_stream(invoke_chat_history(chain1,chat_session_id,prompt_input1))
    st.session_state.prev_chat_history.append({'role':'assistant',"content":ai_response1})
    #st.write(ai_response1)

