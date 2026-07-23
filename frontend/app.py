import requests
import streamlit as st

API_URL = "http://localhost:8000"
DEFAULT_MODEL = "llama3.2:3b"

st.set_page_config(page_title="Ollama Local AI Assistant", page_icon="🦙")
st.title("🦙 Ollama Local AI Assistant")
st.caption("Private local AI chat using Ollama, FastAPI, and Streamlit")

with st.sidebar:
    model = st.text_input("Ollama model", value=DEFAULT_MODEL)
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask your local AI assistant...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={"model": model, "messages": st.session_state.messages},
                timeout=190,
            )
            response.raise_for_status()
            answer = response.json()["content"]
        except requests.exceptions.ConnectionError:
            answer = "Backend is not running. Start it with: `python -m uvicorn backend.main:app --reload`"
        except requests.exceptions.HTTPError:
            try:
                answer = f"Backend error: {response.json().get('detail')}"
            except Exception:
                answer = f"Backend error: {response.text}"
        except requests.exceptions.Timeout:
            answer = "The model timed out. Try a smaller model."
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
