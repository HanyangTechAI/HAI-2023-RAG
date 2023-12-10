import os
import gettext

import streamlit as st

from llm import get_generation_prompt, generate
from search import store_file_to_db, store_webpage_to_db, search, delete

languages = ["en", "ko"]
localizator = gettext.translation(
    "base",
    localedir=os.path.join(os.path.dirname(__file__), "locales"),
    languages=[st.session_state.language if "language" in st.session_state else "en"],
)
localizator.install()
_ = localizator.gettext

st.set_page_config(
    page_title=_("HAI ChatBot Demo"),
    layout="wide",
)

if "language" not in st.session_state:
    st.session_state.language = "en"
if "collection_name" not in st.session_state or st.session_state.collection_name == "":
    st.session_state.collection_name = "default"

st.title(_("🎈 HAI RAG demo"))
col_stat, col_lang = st.columns([1, 1])
col_stat.subheader(_("Currently logged in `{}`").format(st.session_state.collection_name))
language = col_lang.radio(
    _("Select the language of the model"),
    languages,
    index=languages.index(st.session_state.language),
    key="language",
    horizontal=True,
)

system_message = _("You are a chatbot that answers questions accurately and concisely based on the information you are given.")
rag_message = _("Use the above information to answer the following query below:")

expander_cont = st.container()
info_cont = st.container()

with expander_cont.expander("", expanded=True):
    col0, col1 = st.columns([1, 1])
    col0.subheader(_("Settings for semantic search"))
    with col0.form(_("Settings for semantic search"), clear_on_submit=False):
        col_lang, col_name = st.columns([1, 1])
        collection_name = st.text_input(
            label=_("Enter the name of database to use."), key="collection_name"
        )
        top_k = st.slider(
            _("Select the number of references to use"), 0, 10, 3, key="top_k"
        )

        col_update, col_delete, col_clear = st.columns([1, 1, 1])
        update_setting_button = col_update.form_submit_button(_("Update"))
        clear_db_button = col_delete.form_submit_button(_("Clear DB"))
        clear_history_button = col_clear.form_submit_button(_("Clear Chat History"))
        
        if update_setting_button:
            info_cont.success(_("Settings updated"))

        if clear_db_button:
            try:
                result = delete(collection_name)
                if result:
                    info_cont.success(_("Collection {} delete success").format(collection_name))
                else:
                    info_cont.warning(_("Collection {} delete failed.").format(collection_name))
            except:
                info_cont.error(
                    _("Error occured while deleting collection {}.").format(collection_name)
                )
                
        if clear_history_button:
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": system_message,
                    "reference": "",
                }
            ]

    col1.subheader(_("Upload documents for AI to reference"))
    col1.markdown(
        _(
            "- Once the file or webpage is entered, it is automatically split into pages and stored in the DB.\n- When you type a "
            "question, it will answer based on the most relevant pages."
        )
    )
    input_type = col1.radio("Input Type", [_("File"), _("Webpage")], label_visibility="collapsed")
    with col1.form(_("Upload File"), clear_on_submit=False):
        if input_type == _("File"):
            uploaded_file = st.file_uploader(
                _("Uplode files"),
                ["txt", "pdf", "docx", "xlsx", "pptx", "hwp"],
                accept_multiple_files=False,
                label_visibility="hidden",
            )
            webpage_url = None
        else:
            uploaded_file = None
            webpage_url = st.text_input("URL", placeholder=_("Enter the URL of webpage to use"))

        submit_button = st.form_submit_button(_("Submit"))
        if submit_button:
            if uploaded_file:
                try:
                    result = store_file_to_db(collection_name, uploaded_file, language)
                    if result:
                        info_cont.success(_("File {} upload success").format(uploaded_file.name))
                    else:
                        info_cont.warning(_("File {} upload failed.").format(uploaded_file.name))
                except:
                    info_cont.error(_("Error occured while uploading file {}.").format(uploaded_file.name))
            elif webpage_url:
                try:
                    result = store_webpage_to_db(collection_name, webpage_url, language)
                    if result:
                        info_cont.success(_("Webpage {} upload success").format(webpage_url))
                    else:
                        info_cont.warning(_("Webpage {} upload failed.").format(webpage_url))
                except:
                    info_cont.error(_("Error occured while uploading webpage {}.").format(webpage_url))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_message,
            "reference": "",
        }
    ]

st.session_state.messages[0]["content"] = system_message

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if not message["role"] == "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("reference"):
                with st.expander(_("References")):
                    st.markdown(message["reference"])

# React to user input
if prompt := st.chat_input(_("How can I help you today?")):
    # Display user message in chat message contain
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "reference": ""}
    )

    search_results = search(st.session_state.collection_name, prompt, language, top_k)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # Change prompt into chat format
        prompt = get_generation_prompt(
            st.session_state.messages, search_results, rag_message
        )

        full_response = ""
        for chunk in generate(prompt):
            full_response += chunk[0]
            message_placeholder.markdown(full_response + "▌")
        full_response = chunk[1].rstrip("<|user|>")
        message_placeholder.markdown(full_response)

        reference_text = ""
        if search_results:
            with st.expander(_("References")):
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
