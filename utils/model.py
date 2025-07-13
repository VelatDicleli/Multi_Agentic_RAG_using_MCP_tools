from langchain_groq import ChatGroq
from dotenv import load_dotenv
from logger import logging

load_dotenv()

llm = ChatGroq(model="qwen/qwen3-32b")

router_llm = ChatGroq(model="deepseek-r1-distill-llama-70b")  

