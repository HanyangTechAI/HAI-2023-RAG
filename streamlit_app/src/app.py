import streamlit as st

from llm import get_generation_prompt, generate
from search import store_file_to_db, search, delete

st.set_page_config(
    page_title="HAI ChatBot Demo",
    layout="wide",
)

if "collection_name" not in st.session_state or st.session_state.collection_name == "":
    st.session_state.collection_name = "default"
if "system_message" not in st.session_state:
    st.session_state.system_message = (
        "You are a chatbot that always answers with kindness and detail."
    )
if "top_k" not in st.session_state:
    st.session_state.top_k = 3

st.title("🎈 HAI RAG demo")

col0, col1 = st.columns([1, 1])

with col0.form("Settings", clear_on_submit=False):
    st.subheader(f"Currently logged in `{st.session_state.collection_name}`")
    collection_name = st.text_input(
        label="Enter the name of database to use.", key="collection_name"
    )
    st.text_area(
        "Input system messages below:", key="system_message", label_visibility="visible"
    )
    top_k = st.slider("Select the number of references to use", 0, 10, 3, key="top_k")
    clear_db_button = st.form_submit_button("Clear DB")

if clear_db_button:
    try:
        result = delete(collection_name)
        if result:
            st.success(f"Collection {collection_name} deleted")
        else:
            st.warning(f"Collection {collection_name} delete failed.")
    except:
        st.error(f"Error occured while deleting collection {collection_name}.")

with col1.form("Upload File", clear_on_submit=False):
    st.subheader("Upload documents for AI to reference")
    st.markdown(
        "- Once the file is entered, it is automatically split into pages and stored in the DB.\n- When you type a "
        "question, it will answer based on the most relevant pages."
    )
    uploaded_file = st.file_uploader(
        "Uplode files",
        ["pdf", "docx", "pptx", "hwp", "txt"],
        accept_multiple_files=False,
        label_visibility="hidden",
    )
    submit_button = st.form_submit_button("Submit")

if submit_button and uploaded_file:
    try:
        result = store_file_to_db(collection_name, uploaded_file)
        if result:
            st.success(f"File {uploaded_file.name} upload success")
        else:
            st.warning(f"File {uploaded_file.name} upload failed.")
    except:
        st.error(f"Error occured while uploading file {uploaded_file.name}.")

# Initialize chat histor
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": st.session_state.system_message,
            "reference": "",
        }
    ]

st.session_state.messages[0]["content"] = st.session_state.system_message

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if not message["role"] == "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("reference"):
                with st.expander("References"):
                    st.markdown(message["reference"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message contain
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "reference": ""}
    )

    search_results = search(st.session_state.collection_name, prompt, top_k)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # Change prompt into chat format
        prompt = get_generation_prompt(st.session_state.messages, search_results)

        full_response = ""
        for chunk in generate(prompt):
            full_response += chunk[0]
            message_placeholder.markdown(full_response + "▌")
        full_response = chunk[1]
        message_placeholder.markdown(full_response)

        reference_text = ""
        if search_results:
            with st.expander("References"):
                reference_text += "---\n\n"
                for i, sr in enumerate(search_results):
                    sr_text = f"##### Reference {i + 1}\n"
                    for k, v in sr["metadata"].items():
                        sr_text += f"- **{k}**: {v}\n"
                    sr_text += f"```text\n{sr['document']}\n```\n"
                    reference_text += sr_text
                st.markdown(reference_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response, "reference": reference_text}
    )
