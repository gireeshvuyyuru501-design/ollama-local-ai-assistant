# Ollama Local AI Assistant

A small GitHub-ready project using Ollama, FastAPI, and Streamlit.

## Features
- Local LLM chat
- FastAPI backend
- Streamlit frontend
- Conversation history
- Model selector
- No paid API key required for local Ollama

## Run on Windows

### 1. Install Ollama
Install and open Ollama.

### 2. Pull a model
```powershell
ollama pull llama3.2:3b
```

For a smaller model:
```powershell
ollama pull gemma3:1b
```

### 3. Set up Python
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### 4. Start backend
Open terminal 1:
```powershell
.venv\Scripts\activate
python -m uvicorn backend.main:app --reload
```

API docs:
```text
http://127.0.0.1:8000/docs
```

### 5. Start frontend
Open terminal 2:
```powershell
.venv\Scripts\activate
python -m streamlit run frontend\app.py
```

App:
```text
http://localhost:8501
```

## GitHub commands
```powershell
git init
git add .
git commit -m "Build Ollama local AI assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ollama-local-ai-assistant.git
git push -u origin main
```

## Resume bullet
Built a privacy-focused local AI assistant using Ollama, FastAPI, and Streamlit, integrating a local language model through REST APIs with conversational memory and model selection.
