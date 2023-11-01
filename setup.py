import streamlit as st
from sqlalchemy import create_engine, text, Index
from sqlalchemy.orm import sessionmaker
from models import Base, EmbeddingsDemo, QAEmbeddingsDemo

db_url = st.secrets["POSTGRES_DATABASE_URL"]
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def create_pg_vector_extension():
    session = Session()
    try:
        create_extension_query = text("CREATE EXTENSION IF NOT EXISTS vector;")
        session.execute(create_extension_query)
        session.commit()
        print("Extension 'vector' created (if it didn't exist)")
    except Exception as e:
        print(f"Error creating vector extension: {e}")
    finally:
        session.close()


def create_database_tables():
    session = Session()
    try:
        Base.metadata.create_all(engine)
        print("Successfully created database tables")
    except Exception as e:
        print(f"Error creating the tables: {e}")
    finally:
        session.close()


embeddings_demo_column_embedding_vector_idx = Index(
    "embeddings_demo_column_embedding_vector_idx",
    EmbeddingsDemo.embedding_vector,
    postgresql_using="ivfflat",
    postgresql_with={"lists": 100},
    postgresql_ops={"embedding": "vector_cosine_ops"},
)

qa_embeddings_demo_column_question_embedding_vector_idx = Index(
    "qa_embeddings_demo_column_question_embedding_vector_idx",
    QAEmbeddingsDemo.question_embedding_vector,
    postgresql_using="ivfflat",
    postgresql_with={"lists": 100},
    postgresql_ops={"embedding": "vector_cosine_ops"},
)


def create_table_indexes():
    embeddings_demo_column_embedding_vector_idx.create(
        bind=engine,
        checkfirst=True,
    )
    qa_embeddings_demo_column_question_embedding_vector_idx.create(
        bind=engine,
        checkfirst=True,
    )
    print("Successfully created table indexes")


if __name__ == "__main__":
    create_pg_vector_extension()
    create_database_tables()
    create_table_indexes()
