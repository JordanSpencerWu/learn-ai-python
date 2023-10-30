from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class EmbeddingsDemo(Base):
    __tablename__ = "embeddings_demo"
    id = Column(Integer, primary_key=True)
    prompt = Column(String, unique=True)
    embedding_vector = Column(Vector(1536))
