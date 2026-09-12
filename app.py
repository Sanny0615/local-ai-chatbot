import streamlit as st
import ollama

st.title("🤖 My Local AI Chatbot")

# Sidebar
with st.sidebar:
    st.header("Settings")

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
question = st.chat_input("Ask me something...")

if question:

    st.chat_message("user").write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": """
            You are a helpful beginner-friendly AI tutor.
            Keep answers concise and simple.
            First explain the main concept.
            Then give 2 important points.
            Then give 1 simple example.
            Do not give unnecessary information.
            If the user asks for more detail, then explain more.
            """
        },
        *st.session_state.messages
    ],
    options={
        "temperature": temperature
    }
  )

    answer = response["message"]["content"]

    st.chat_message("assistant").write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })