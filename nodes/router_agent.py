from typing import Literal
from pydantic import BaseModel
from utils.model import router_llm
from core.state import RAGstate
from langchain_core.messages import SystemMessage, HumanMessage

class Route(BaseModel):
    step: Literal["websearch", "documentsearch", "geography"]

llm = router_llm.with_structured_output(Route)

async def router_agent(state: RAGstate):
   
    last_message = state["messages"][-1]
    
 
    messages = [
        SystemMessage(
            content="""You are a router agent responsible for directing user queries to the most appropriate tool among the following options: web search, document search, or geography knowledge base.

                Your task is to carefully analyze the user's input and determine which tool can best provide the correct and relevant answer.

                - If the user’s question requires up-to-date information or facts not found in the document database, route to **web search**.
                - If the question is about information contained within the uploaded or indexed documents, route to **document search**.
                - If the question specifically involves geographical information, locations, maps, or spatial data, route to the **geography knowledge base**.
                - If the query is ambiguous, choose the tool that is most likely to provide a relevant and accurate answer.
                - Always focus on routing to the tool that maximizes answer quality and relevance.
                
                Make your routing decision based only on the user's request content."""

        ),
                last_message 
    ]
    
    try:
        decision = await llm.ainvoke(messages)
        return {"decision": decision.step}
    except Exception as e:
        print(f"Error in router_agent: {e}")
        
        return {"decision": "documentsearch"}