"""
@chain is a decorative which can be used for the same purpose as RunnableLambda. We can make
our custom method into a Runnable by marking it using @chain and directly pass it in the chain calling
"""
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain

## Setup Env variables and LangSmith tracing
load_dotenv()

## Initialize the llms
llm1 = ChatOllama(
    base_url="http://localhost:11434",
    model="qwen2.5:latest",
    temperature=0.3
)
llm2 = ChatOllama(
    base_url="http://localhost:11434",
    model="deepseekr1:8b",
    temperature=0.3
)
slm1 = ChatOllama(
    base_url="http://localhost:11434",
    model="gemma3:1b",
    max_tokens=300
)
#### Custom chain
@chain
def choose_llm(response):
    if len(str(response)) < 500:
        print("Generating the response from Gemma3 model.....")
        return slm1
    print("Generating the response from latest Qwen2.5 model.....")
    return llm1


### Create prompts
prompt1 = ChatPromptTemplate.from_template("What are the steps to land a job as Software AI QA at {company_name}?")

prompt2 = ChatPromptTemplate.from_template("Analyse the {p1_response} and give me the step names only")

# chain 1
first_chain = prompt1 | llm1 | StrOutputParser()
# chain 2
second_chain = {"p1_response":first_chain} | prompt2 | choose_llm | StrOutputParser()
final_response = second_chain.invoke({"company_name":"Fidelity Investments"})
print(final_response)

