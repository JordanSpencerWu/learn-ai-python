import openai
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import QAEmbeddingsDemo

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai_embeddings_model = st.secrets["OPENAI_EMBEDDINGS_MODEL"]
db_url = st.secrets["POSTGRES_DATABASE_URL"]

st.set_page_config(page_title="Storing QA Embeddings Demo")

st.info(
    f"Using {openai_embeddings_model} model to change modify OPENAI_EMBEDDINGS_MODEL in .streamlit/secrets.toml file",
    icon="ℹ️",
)

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


def generate_embeddings(prompt):
    return openai.Embedding.create(model=openai_embeddings_model, input=prompt)


default_question = """\
What's the color of the sky?
"""

default_answer = """\
The sky is blue.
"""

try:
    with st.form("storing_qa_embeddings_form"):
        question = st.text_area("Enter question:", value=default_question, height=100)
        answer = st.text_area("Enter answer:", value=default_answer, height=100)

        submitted = st.form_submit_button("Generate Embeddings and Save")
        if submitted:
            question = question.strip()
            answer = answer.strip()
            embeddings = generate_embeddings(question)
            embedding = embeddings["data"][0]["embedding"]
            new_record = QAEmbeddingsDemo(
                answer=answer, question=question, question_embedding_vector=embedding
            )
            session.add(new_record)
            session.commit()
            st.success("Successfully saved embeddings")
except Exception as e:
    session.rollback()
    st.error(f"Failed to save embeddings: {e}")
finally:
    session.close()
