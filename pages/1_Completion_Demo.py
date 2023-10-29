import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_model = st.secrets["OPENAI_MODEL"]

st.set_page_config(page_title="Completion Demo")

st.info(
    f"Using {openai_model} model to change modify OPENAI_MODEL in .streamlit/secrets.toml file",
    icon="ℹ️",
)


def generate_response(prompt):
    completion = openai.ChatCompletion.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )
    st.info(completion.choices[0].message["content"])


zero_shot_prompt = """\
Classify the text into neutral, negative or positive. 
Text: I think the vacation is okay.
Sentiment:
"""

with st.form("completion_form"):
    text = st.text_area("Enter prompt:", zero_shot_prompt)
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
