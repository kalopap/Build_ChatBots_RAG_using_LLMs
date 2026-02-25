from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from sqlalchemy import create_engine

## Setup Env variables and LangSmith tracing
load_dotenv()

### Initialize the LLM
llm1 = ChatOllama(
    model="qwen2.5:latest",
    base_url="http://localhost:11434",
    temperature=0,
)

## Create prompts
system_prompt1 = "You are an expert dietician for body weight control"

diet_prompt1 = "I feel hungry all the time. How do I control my apetite?"

diet_followup_prompt2 = "Can you suggest a health vegetarian 3 day meal plan. Don't give the recipe details, just the names. Indian preferred"

diet_followup_prompt3 = "What do you know about me?"

### Create Prompt Template

diet_prompt_template = ChatPromptTemplate.from_messages([
    ("system",system_prompt1),
    ("placeholder","{diet_history_key}"),
    ("user","{diet_prompt_key}")

])

### Assign the chain 
diet_chain = diet_prompt_template | llm1 | StrOutputParser()

### Establish Session for user
diet_store = {}

#Alternative to connection_string
diet_engine = create_engine("sqlite:///diet_chathistory.db")

def get_diet_session_history(session_id):
    return SQLChatMessageHistory(session_id=session_id,connection=diet_engine)
    #return SQLChatMessageHistory(session_id=session_id,connection_string="sqlite:///diet_chathistory.db")
    

#### to Configure history to the prompts, create a RunnableWithMessageHistory object
diet_history = RunnableWithMessageHistory(
    diet_chain,
    get_diet_session_history,
    input_messages_key="diet_prompt_key",
    history_messages_key="diet_history_key"
)
### Empty the session before invoking history

dsession_id = "KalyaniBot"

get_diet_session_history(dsession_id).clear()

#### Invoke the prompts with history

diet_response_from_llm1 = diet_history.invoke(
    {"diet_prompt_key": diet_prompt1},
    config={"configurable":{"session_id":dsession_id}}
)
print(diet_response_from_llm1)
print("------------------------Answering the followup question------------")

diet_followup_response2 = diet_history.invoke(
    {"diet_prompt_key": diet_followup_prompt2},
    config={"configurable":{"session_id":dsession_id}}
)
print(diet_followup_response2)
print("------------------------Answering the followup question 2-----------")

diet_followup_response3 = diet_history.invoke(
    {"diet_prompt_key": diet_followup_prompt3},
    config={"configurable":{"session_id":dsession_id}}
)
print(diet_followup_response3)