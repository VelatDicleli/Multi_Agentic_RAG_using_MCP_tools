# import asyncio
# from utils.load_docs import load_docs
# from core.graph import build_graph
# from langchain_core.messages import HumanMessage


# async def run():

#     # load_docs(r"C:\Users\User\Desktop\agentic_rag\Velat_Dicleli_cv.pdf")
#     graph = await build_graph()

#     initial_state = {
#         "messages": [HumanMessage(content="bu dokumandaki kişinin becerileri nelerdi")],
#     }
    
#     config = {
#         "configurable": {
#             "thread_id": "2"
#         }
#     }


#     result = await graph.ainvoke(initial_state,config)
#     print(result["messages"][-1].content)
    

# if __name__ == "__main__":
#     asyncio.run(run())



import asyncio
from utils.load_docs import load_docs
from core.graph import build_graph
from langchain_core.messages import HumanMessage
from utils.store import vector_store


async def run():
    graph = await build_graph()
  
    thread_id = "6"

    print("Çıkmak için 'exit' yazınız.")

    while True:
        user_input = input("Soru: ")
        if user_input.lower() in ["exit", "çıkış", "quit"]:
            print("Programdan çıkılıyor...")
            break

        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            
        }

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = await graph.ainvoke(initial_state, config)
        print("Cevap:", result["messages"][-1].content)
        


if __name__ == "__main__":
    # vector_store.delete(delete_all=True)
    asyncio.run(run())
    
