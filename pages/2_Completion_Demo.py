import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_model = st.secrets["OPENAI_MODEL"]

st.set_page_config(page_title="Completion Demo")

st.info(
    f"Using {openai_model} model to change modify OPENAI_MODEL in .streamlit/secrets.toml file",
    icon="ℹ️",
)


def generate_chat_completion(prompt):
    return openai.ChatCompletion.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )


default_prompt = """\
Classify the text into neutral, negative or positive. 
Text: I think the vacation is okay.
Sentiment:
"""

with st.form("completion_form"):
    prompt = st.text_area("Enter prompt:", value=default_prompt, height=300)

    submitted = st.form_submit_button("Submit")
    if submitted:
        prompt = prompt.strip()
        chat_completion = generate_chat_completion(prompt)
        st.info(chat_completion.choices[0].message["content"])
