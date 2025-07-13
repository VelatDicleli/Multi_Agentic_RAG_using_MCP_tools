
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from pinecone import ServerlessSpec
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone()

index_name = "rag"  

index = pc.Index(index_name)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = PineconeVectorStore(index=index, embedding=embeddings)



