import streamlit as st
from llmapi import get_generation_prompt, generate

st.set_page_config(
        page_title="HAI ChatBot Demo",
)

st.title('🎈 HAI Chatbot demo')

with st.form("Upload File"):
    uploaded_file = st.file_uploader("Enter a file that the AI will use to reference in its answer.",
                                     ["pdf", "docx", "hwp", "txt"],
                                     accept_multiple_files=False
                                    )
    st.form_submit_button("Submit")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
# Initialize chat histor
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a chatbot that always answers with kindness and detail.
If a question is asked in English, make sure to answer in English.
If a question is asked in Korean, make sure to answer in Korean.""",
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if not message["role"] == "system":
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
        
        # Change prompt into chat format
        prompt = get_generation_prompt(st.session_state.messages)
        
        full_response = ""
        for chunk in generate(prompt):
            full_response += chunk[0]
            message_placeholder.markdown(full_response + "▌")
        full_response = chunk[1]
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
