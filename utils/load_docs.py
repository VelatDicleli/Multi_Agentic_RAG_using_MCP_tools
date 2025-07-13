import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.store import vector_store
import logging

logging.basicConfig(level=logging.INFO)

async def load_docs(file_path: str):
  
    try:
     
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

       
        if os.path.getsize(file_path) < 1000:  
            raise ValueError("File is too small or empty")

   
        loader = PyPDFLoader(file_path=file_path)
        docs = await loader.aload()
        
        if not docs:
            raise ValueError("No documents could be loaded from the PDF.")

        logging.info(f"{len(docs)} page(s) loaded from PDF.")

        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=750,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " "],  
        )

        split_docs = text_splitter.split_documents(docs)
        logging.info(f"Document split into {len(split_docs)} chunks.")

        if not split_docs:
            raise ValueError("No content could be split from the document.")

      
        await vector_store.aadd_documents(split_docs)
        logging.info(f"{len(split_docs)} chunks added to the vector store successfully.")

    except Exception as e:
        logging.error(f"Error loading documents: {str(e)}")
        raise
