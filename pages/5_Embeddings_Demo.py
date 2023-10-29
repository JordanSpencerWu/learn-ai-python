import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_embeddings_model = st.secrets["OPENAI_EMBEDDINGS_MODEL"]

st.set_page_config(page_title="Embeddings Demo")

st.info(
    f"Using {openai_embeddings_model} model to change modify OPENAI_EMBEDDINGS_MODEL in .streamlit/secrets.toml file",
    icon="ℹ️",
)


def generate_response(prompt):
    embeddings = openai.Embedding.create(model=openai_embeddings_model, input=prompt)
    st.info(embeddings["data"][0]["embedding"])


prompt = """\
Food
"""

with st.form("embeddings_form"):
    text = st.text_area("Enter prompt:", prompt)
    submitted = st.form_submit_button("Generate Embeddings")
    if submitted:
        generate_response(text)
