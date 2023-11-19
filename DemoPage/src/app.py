import streamlit as st
import openai
from llmapi import createTokens

st.set_page_config(
        page_title="HAI ChatBot Demo",
)

st.title('🎈 HAI Chatbot demo')
st.write('building...')

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
# Initialize chat histor
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("어떤 도움이 필요하신가요?"):
    # Display user message in chat message contain
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for token in createTokens(prompt):
            full_response += token
            message_placeholder.markdown(full_response + "▌")
            # print(token)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})