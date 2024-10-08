import streamlit as st
from typing import Generator

# Assuming Groq is a valid API service
from groq import Groq  

st.image('logo.png')
st.write("Hello! I'm your friendly Coding chatbot. I can help answer your questions, provide information. I'm also super fast! Let's start our conversation!")

client = Groq(
    api_key='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', 
)

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.chat.completions.create(
            model='Llama-3.2-90b-text-preview',  # Check model name
            messages=[{
                "role": m["role"],
                "content": m["content"]
            } for m in st.session_state.messages],
            stream=True
        )

        # Use a placeholder for streaming responses
        response_placeholder = st.empty()
        chat_responses_generator = generate_chat_responses(chat_completion)

        full_response = ""
        for chunk in chat_responses_generator:
            full_response += chunk
            response_placeholder.markdown(full_response)  # Update the response live

    except Exception as e:
        st.error(str(e), icon="🚨")

    # Append the full response to session_state.messages
    st.session_state.messages.append({"role": "assistant", "content": full_response})
