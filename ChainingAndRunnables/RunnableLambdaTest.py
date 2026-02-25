from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

## Setup Env variables and LangSmith tracing
load_dotenv()

## Initialize the LLMs
llm1 = ChatOllama(
    base_url="http://localhost:11434",
    model="qwen2.5:latest",
    max_tokens=300,
    temperature=0.3
)
llm2 = ChatOllama(
    base_url="http://localhost:11434",
    model="deepseek-r1:8b",
    temperature=0.3,
    max_tokens=300
)
slm1 = ChatOllama(
    model="gemma3:1b",
    base_url="http://localhost:11434",
    temperature=0.3,
    max_tokens = 250

)

def choose_llm(response):
    response_text = str(response)
    if len(response_text) > 500:
        print("Using the Qwen2.5 latest model to generate response......")
        return llm1
    print("Using the small Gemma3 model to generate response.......")
    return slm1

##### Create Prompts ########

#1
qa_prompt1 = ChatPromptTemplate([
    ("system","You are {role} looking to transition to AI world"),
    ("user", "Which is the top role(with less code and less steps to reach) in AI world will you pick if you have 2 months only?")
])
#2
career_prompt2 = ChatPromptTemplate.from_template(
    """  Analyse the {qa_response} and prepare a short 2 month roadmap for that role without deep ML"""
)

#chain 1
qa_chain1 = qa_prompt1 | llm1 | StrOutputParser()
#choose llm based on the response
llm_selector = RunnableLambda(choose_llm)
# pass the output of chain1 to chain2
roadmap_chain2 = {"qa_response":qa_chain1} | career_prompt2 | llm_selector | StrOutputParser()
response = roadmap_chain2.invoke({"role":"QA Automation engineer"})
print(response)


    