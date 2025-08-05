import streamlit as st
import requests

# st.set_page_config must be the first Streamlit command
st.set_page_config(page_title="Groq Chatbot", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center; color: #4A90E2;'>🧠 Groq Chatbot</h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by Mixtral + FastAPI + Streamlit</p>",
    unsafe_allow_html=True
)
st.divider()

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you today?"}]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
user_input = st.chat_input("Type your message here Dulith...")

# Send and receive
if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show assistant thinking placeholder
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ Thinking...")

    # Send message to FastAPI
    try:
        res = requests.post("http://127.0.0.1:8000/chat", json={"messages": st.session_state.messages})
        res.raise_for_status()
        reply = res.json()["response"]
    except requests.exceptions.RequestException as e:
        reply = f"⚠️ **Error:** {str(e)}"

    # Update assistant message
    placeholder.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})


