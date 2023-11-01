import openai
import streamlit as st
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import QAEmbeddingsDemo

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


default_question = """\
What's the color of the sky?
"""

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

with st.form("query_embeddings_form"):
    question = st.text_area("Enter question:", value=default_question, height=100)

    submitted = st.form_submit_button("Query")
    if submitted:
        question = question.strip()
        embeddings = generate_embeddings(question)
        embedding = embeddings["data"][0]["embedding"]

        qa_embedding_demos = session.scalars(
            select(QAEmbeddingsDemo)
            .filter(
                QAEmbeddingsDemo.question_embedding_vector.cosine_distance(embedding)
                < 0.1
            )
            .order_by(
                QAEmbeddingsDemo.question_embedding_vector.cosine_distance(embedding)
            )
            .limit(1)
        )

        for qa_embedding_demo in qa_embedding_demos:
            st.info(qa_embedding_demo.answer)
