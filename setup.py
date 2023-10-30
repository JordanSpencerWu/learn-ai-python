import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base

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


create_embeddings_demo_table_sql = text(
    """
    CREATE IF NOT EXISTS TABLE EmbeddingsDemo (
        id SERIAL PRIMARY KEY,
        prompt TEXT UNIQUE,
        embedding_vector vector(1536)
    );

    CREATE UNIQUE INDEX unique_prompt_index ON EmbeddingsDemo (prompt);
    """
)


def create_database_tables():
    session = Session()
    try:
        Base.metadata.create_all(engine)
        print("Successfully created database tables")
    except Exception as e:
        print(f"Error creating the tables: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    create_pg_vector_extension()
    create_database_tables()
