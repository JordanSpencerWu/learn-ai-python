import openai
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import EmbeddingsDemo

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_embeddings_model = st.secrets["OPENAI_EMBEDDINGS_MODEL"]
db_url = st.secrets["POSTGRES_DATABASE_URL"]

st.set_page_config(page_title="Storing Embeddings Demo")

st.info(
    f"Using {openai_embeddings_model} model to change modify OPENAI_EMBEDDINGS_MODEL in .streamlit/secrets.toml file",
    icon="ℹ️",
)

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


def generate_embeddings(prompt):
    return openai.Embedding.create(model=openai_embeddings_model, input=prompt)


prompt = """\
Food
"""

try:
    with st.form("embeddings_form"):
        prompt = st.text_area("Enter prompt:", prompt)

        submitted = st.form_submit_button("Generate Embeddings and Save")
        if submitted:
            embeddings = generate_embeddings(prompt)
            embedding = embeddings["data"][0]["embedding"]
            new_record = EmbeddingsDemo(prompt=prompt, embedding_vector=embedding)
            session.add(new_record)
            session.commit()
            st.success("Successfully saved embeddings")
except Exception as e:
    session.rollback()
    st.error(f"Failed to save embeddings: {e}")
finally:
    session.close()
