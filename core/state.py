from typing import Annotated, List, Optional, TypedDict
from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class RAGstate(TypedDict):
    messages: Annotated[list,add_messages]
    decision: Optional[str]


