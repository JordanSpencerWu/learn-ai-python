import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_model = st.secrets["OPENAI_MODEL"]

st.set_page_config(page_title="Chat Demo")

st.info(
    f"Using {openai_model} model to change modify OPENAI_MODEL in .streamlit/secrets.toml",
    icon="ℹ️",
)


def generate_chat_completion(messages):
    return openai.ChatCompletion.create(
        model=openai_model,
        messages=messages,
        stream=True,
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    prompt = prompt.strip()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages = [
            {"role": "assistant", "content": "You are a helpful support specialist."}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[-5:]
        ]
        for chat_completion in generate_chat_completion(messages):
            full_response += chat_completion.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
