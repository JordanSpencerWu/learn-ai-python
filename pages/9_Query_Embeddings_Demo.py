import openai
import streamlit as st
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import EmbeddingsDemo

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_embeddings_model = st.secrets["OPENAI_EMBEDDINGS_MODEL"]
db_url = st.secrets["POSTGRES_DATABASE_URL"]

st.set_page_config(page_title="Querying Embeddings Demo")

st.info(
    f"Using {openai_embeddings_model} model to change modify OPENAI_EMBEDDINGS_MODEL in .streamlit/secrets.toml file",
    icon="ℹ️",
)


def generate_embeddings(prompt):
    return openai.Embedding.create(model=openai_embeddings_model, input=prompt)


default_prompt = """\
Fruit
"""

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

with st.form("query_embeddings_form"):
    prompt = st.text_area("Enter query:", value=default_prompt, height=300)
    nearest_neighbors = st.selectbox(
        "Select number of nearest neighbors", ("1", "5", "10"), index=1
    )

    submitted = st.form_submit_button("Query")
    if submitted:
        prompt = prompt.strip()
        embeddings = generate_embeddings(prompt)
        embedding = embeddings["data"][0]["embedding"]

        embedding_demos = session.scalars(
            select(EmbeddingsDemo)
            .filter(EmbeddingsDemo.embedding_vector.cosine_distance(embedding) < 0.15)
            .order_by(EmbeddingsDemo.embedding_vector.cosine_distance(embedding))
            .limit(nearest_neighbors)
        )

        for embedding_demo in embedding_demos:
            st.info(embedding_demo.prompt)
