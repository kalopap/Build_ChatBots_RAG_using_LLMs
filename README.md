# 🤖 1. Basic Chatbot with LangChain & Streamlit

---

## 📌 About This Project

This is a hands-on project built while learning how Large Language Models (LLMs) work in practice. 
The goal of this project is to understand the foundational building blocks of a conversational AI application — from basic LLM API calls 
to a fully functional chatbot with a UI and persistent conversation history.

---

## 🗂️ Project Structure

```
Build_ChatBots_RAG_using_LLMs/
│
├── BasicSetup/              # Initial LLM setup and API connection experiments
├── BuildChatBot/            # Streamlit chatbot application
├── ChainingAndRunnables/    # LangChain LCEL chains and runnables exploration
├── ChatMessageHistory/      # Conversation history persistence with SQLite
│
├── user_chathistory.db      # SQLite DB for storing user chat history
├── diet_chathistory.db      # SQLite DB for a diet-focused chatbot session
├── .gitignore
└── README.md
```

---

## ✨ Features

- 💬 **Conversational Chatbot UI** built with Streamlit
- 🧠 **LLM Integration** via LangChain (supports OpenAI & Ollama for local models)
- 📝 **Persistent Conversation History** using SQLite
- 🔗 **LangChain Chains & Runnables** (LCEL) for composing LLM pipelines
- 🔍 **LangSmith Tracing** for monitoring and debugging LLM runs
- 🆕 **New Chat** button to reset and start fresh sessions
- 📂 **Sidebar** for navigation and session controls

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Streamlit** | Frontend UI for the chatbot |
| **LangChain** | LLM orchestration, chaining, and memory |
| **Ollama** | Running LLMs locally (e.g., LLaMA, Mistral) |
| **LangSmith** | Tracing and observability for LLM runs |
| **SQLite** | Persistent chat history storage |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/kalopap/Build_ChatBots_RAG_using_LLMs.git
cd Build_ChatBots_RAG_using_LLMs
```

### 2. Install Dependencies

```bash
pip install streamlit langchain langchain-openai langchain-ollama langsmith python-dotenv
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ChatBot-POC
```

### 4. (Optional) Set Up Ollama for Local LLM

Download and install [Ollama](https://ollama.com), then pull a model:

```bash
ollama pull llama3
```

### 5. Run the Chatbot

```bash
streamlit run BuildChatBot/app.py
```

---

## 📚 What I Learned

- How LLMs process prompts and generate responses via API calls
- How to structure **prompt templates** using LangChain
- How **LCEL (LangChain Expression Language)** chains work with the `|` pipe operator
- How to maintain **conversation context** using `ChatMessageHistory`
- How to persist chat history to a **SQLite database**
- How to build an interactive chatbot UI using **Streamlit**
- How to trace and debug LLM calls using **LangSmith**

---

##  Author

**Kalyani Kopparapu**
- GitHub: [@kalopap](https://github.com/kalopap)

---

## 📄 License

This project is for learning and portfolio purposes.
