
from contextlib import asynccontextmanager
import os
import tempfile
import uuid
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.load_docs import load_docs
from core.graph import build_graph
from langchain_core.messages import HumanMessage
from utils.store import vector_store



class QueryRequest(BaseModel):
    query: str

  
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.graph = await build_graph()
    app.state.session_id = str(uuid.uuid4()) 
    
    yield  

    app.state.session_id = None

    
    
 
app = FastAPI(lifespan=lifespan)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
     
        contents = await file.read()
       
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

       
        await load_docs(file_path=tmp_path)

        return {"filename": file.filename, "message": "File uploaded and processed successfully."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/delete_store")
async def delete_all():

    try:
        if vector_store:
            await vector_store.adelete(delete_all=True)

            new_session = str(uuid.uuid4())
            app.state.session_id = new_session
            return {
                "status": "success",
                "message": "Vector store deleted.",
                "new_session_id": new_session
            }
        else:
            raise HTTPException(status_code=404, detail="Vector store not initialized.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vector store: {str(e)}")

    

@app.post("/ask")
async def ask_agent(request: Request, body: QueryRequest):
    graph = request.app.state.graph
    session_id = request.app.state.session_id

  

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    initial_state = {
        "messages": [HumanMessage(content=body.query)],
    }

    result = await graph.ainvoke(initial_state, config)

    return {"answer": result["messages"][-1].content}

    


@app.get("/reset_chat_history_id")
def reset_session(request: Request):
    new_sid = str(uuid.uuid4())
    request.app.state.session_id = new_sid
    return {"new_session_id": new_sid}
