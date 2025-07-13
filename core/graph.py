from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from core.state import RAGstate
from nodes.router_agent import router_agent
from nodes.geography_agent import geo_agent
from nodes.websearch_agent import web_agent
from nodes.vector_search_agent import vector_agent
from dotenv import load_dotenv
from langsmith import traceable


load_dotenv()

@traceable
async def build_graph():

    async with AsyncRedisSaver.from_conn_string("redis://127.0.0.1:6379") as checkpointer:
        
        await checkpointer.asetup()
        
        builder = StateGraph(RAGstate)
        
        
        builder.add_node("router_agent",router_agent)
        builder.add_node("web_agent",web_agent)
        builder.add_node("geo_agent",geo_agent)
        builder.add_node("vector_agent",vector_agent)
        
        def route_decision(state: RAGstate):
    
            if state["decision"] == "websearch":
                return "web_agent"
            elif state["decision"] == "documentsearch":
                return "vector_agent"
            elif state["decision"] == "geography":
                return "geo_agent"
        
        builder.add_edge(START,"router_agent")
        builder.add_conditional_edges("router_agent",route_decision, 
        {  
        "web_agent": "web_agent",
        "vector_agent": "vector_agent",
        "geo_agent": "geo_agent",
    },)
        
            
        builder.add_edge("geo_agent",END)
        builder.add_edge("vector_agent",END)
        builder.add_edge("web_agent",END)
 

        graph = builder.compile(checkpointer=checkpointer)
        
        return graph

