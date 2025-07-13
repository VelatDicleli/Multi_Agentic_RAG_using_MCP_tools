from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.store import vector_store
from langchain_core.tools import tool


web_client = MultiServerMCPClient({
    "airbnb": {
        "command": "C:\\Program Files\\nodejs\\npx.cmd",  
        "args": ["-y", "@openbnb/mcp-server-airbnb"],
        "transport": "stdio"
    },
    
    "tavily-mcp": {
        "command": "C:\\Program Files\\nodejs\\npx.cmd",  
        "args": ["-y", "tavily-mcp@0.2.0"],
        "env": {
            "TAVILY_API_KEY": "**********************"
        },
        "transport": "stdio"
    },
    
        "Wikipedia": {
        "command": "C:\\Program Files\\nodejs\\npx.cmd",
        "transport": "stdio",
        "args": ["-y", "wikipedia-mcp"]
        }

})


@tool(description="Retrieves relevant information from the document store based on a user's query.")
def document_tool(query: str) -> str:

    retriever_tool = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 10,
        "lambda_mult": 0.6  
    }
)

    documents = retriever_tool.invoke(query)

    if not documents:
        return "Sorgunuza uygun herhangi bir bilgiye ulaşılamadı."

    
    knowledge = "\n\n".join([doc.page_content.strip() for doc in documents])

    return knowledge

    
geo_client = MultiServerMCPClient({
    "geoMcp":{
        "url": "http://127.0.0.1:8081/mcp",
        "transport": "sse",
     
    }
})
