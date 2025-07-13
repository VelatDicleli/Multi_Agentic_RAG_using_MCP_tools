from tools import web_client
from core.state import RAGstate
from utils.model import llm
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage

async def web_agent(state: RAGstate):
    tools = await web_client.get_tools()
    agent = create_react_agent(model=llm, tools=tools)
    
    try:
       
        response = await agent.ainvoke({"messages": state["messages"]})
       
        if "messages" in response and response["messages"]:
            final_message = response["messages"][-1]
            if isinstance(final_message, AIMessage):
                return {"messages": state["messages"] + [final_message]}
            else:
                return {"messages": state["messages"] + [AIMessage(content=str(final_message.content))]}
        else:
            
            return {"messages": state["messages"] + [AIMessage(content="Web araması tamamlandı ancak sonuç bulunamadı.")]}
    
    except Exception as e:
        print(f"Web agent hatası: {e}")
        return {"messages": state["messages"] + [AIMessage(content=f"Web arama sırasında hata oluştu: {str(e)}")]}