# 🤖 Multi-Agentic RAG with MCP Tools

A sophisticated multi-agent Retrieval-Augmented Generation (RAG) system that leverages Model Context Protocol (MCP) tools for intelligent query routing and response generation. Built with LangGraph for agent orchestration, Pinecone for vector storage, and multiple specialized agents for different query types.

## 🏗️ Architecture

```
                                    ┌─────────────────────┐
                                    │    User Query       │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │    Router Agent     │
                                    │  (DeepSeek R1 70B)  │
                                    └──────────┬──────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
         ┌──────────▼──────────┐    ┌──────────▼──────────┐    ┌──────────▼──────────┐
         │    Web Agent        │    │   Vector Agent      │    │   Geography Agent   │
         │   (Qwen3-32B)       │    │   (Qwen3-32B)       │    │    (Qwen3-32B)      │
         └──────────┬──────────┘    └──────────┬──────────┘    └──────────┬──────────┘
                    │                          │                          │
         ┌──────────▼──────────┐    ┌──────────▼──────────┐    ┌──────────▼──────────┐
         │   MCP Tools         │    │  Pinecone Vector    │    │   MCP Geography     │
         │ • Tavily Search     │    │     Store           │    │      Server         │
         │ • Wikipedia         │    │  (HuggingFace       │    │ • Coordinates       │
         │ • Airbnb            │    │   Embeddings)       │    │ • Distance Calc     │
         └─────────────────────┘    └─────────────────────┘    │ • IP Geolocation    │
                                                               └─────────────────────┘
```

## ✨ Features

- **🔀 Intelligent Query Routing**: DeepSeek R1 70B router agent classifies queries and directs them to the appropriate specialized agent
- **📚 Document RAG**: Upload PDFs and query them using Pinecone vector store with MMR retrieval
- **🌐 Web Search**: Real-time web search via Tavily MCP, Wikipedia, and Airbnb integration
- **🗺️ Geography Tools**: Custom MCP server for geolocation, coordinate lookup, and distance calculations
- **💾 Conversation Memory**: Redis-based checkpointing for persistent chat history
- **🎨 Modern UI**: Streamlit-based chat interface with PDF upload capabilities
- **⚡ Async Architecture**: Fully asynchronous FastAPI backend for high performance

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Agent Framework** | LangGraph, LangChain |
| **LLM (Agents)** | Groq Qwen3-32B |
| **LLM (Router)** | Groq DeepSeek R1 Distill 70B |
| **Vector Store** | Pinecone |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` |
| **Memory** | Redis (AsyncRedisSaver) |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **MCP Tools** | Tavily, Wikipedia, Airbnb, Custom Geography |

## 📁 Project Structure

```
Multi_Agentic_RAG_using_MCP_tools/
├── api.py                      # FastAPI backend endpoints
├── chat_ui.py                  # Streamlit chat interface
├── tools.py                    # MCP client configurations & tools
├── logger.py                   # Logging configuration
├── core/
│   ├── graph.py                # LangGraph workflow definition
│   └── state.py                # State schema for the graph
├── nodes/
│   ├── router_agent.py         # Query classification agent
│   ├── websearch_agent.py      # Web search agent with MCP tools
│   ├── vector_search_agent.py  # Document retrieval agent
│   └── geography_agent.py      # Geography/location agent
├── mcp/
│   └── mcp_server.py           # Custom FastAPI MCP server
├── utils/
│   ├── model.py                # LLM configurations
│   ├── store.py                # Pinecone vector store setup
│   └── load_docs.py            # PDF loading and chunking
└── graph_diagram.png           # Visual representation of the agent graph
```

## 📋 Requirements

- Python 3.10+
- Redis Server
- Node.js (for MCP servers)
- Groq API Key
- Pinecone API Key
- Tavily API Key
- HuggingFace Account

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd Multi_Agentic_RAG_using_MCP_tools
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install MCP servers (Node.js required)

```bash
npm install -g @openbnb/mcp-server-airbnb
npm install -g tavily-mcp@0.2.0
npm install -g wikipedia-mcp
```

### 5. Start Redis

```bash
# Docker
docker run -d -p 6379:6379 redis

# Or local installation
redis-server
```

### 6. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
TAVILY_API_KEY=your_tavily_api_key
HF_TOKEN=your_huggingface_token
```

### 7. Update API keys in `tools.py` and `mcp/mcp_server.py`

Replace placeholder API keys with your actual credentials.

## 🚀 Usage

### Start the Geography MCP Server

```bash
python mcp/mcp_server.py
```
This starts the custom geography MCP server at `http://127.0.0.1:8081`

### Start the FastAPI Backend

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Start the Streamlit UI

```bash
streamlit run chat_ui.py
```

Access the application at `http://localhost:8501`

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask` | POST | Send a query to the multi-agent system |
| `/upload_file` | POST | Upload and process a PDF document |
| `/delete_store` | GET | Clear the vector store |
| `/reset_chat_history_id` | GET | Reset conversation session |

### Example Request

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the distance between Paris and London?"}'
```

## 🔄 Agent Routing Logic

The **Router Agent** analyzes each query and routes to:

| Route | Trigger | Agent |
|-------|---------|-------|
| `websearch` | Current events, real-time info, general knowledge | Web Agent |
| `documentsearch` | Questions about uploaded documents | Vector Agent |
| `geography` | Location, coordinates, distances, maps | Geography Agent |

## 🗺️ Geography MCP Server Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | POST | Get coordinates (lat/lon) for a city |
| `/destination` | POST | Calculate Haversine distance between two points |
| `/ip-to-location` | GET | Get location from IP address |

## 🔧 Configuration

### Vector Store Settings

Modify retrieval parameters in `tools.py`:

```python
retriever_tool = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 10,              # Number of results
        "lambda_mult": 0.6    # MMR diversity factor
    }
)
```

### Document Chunking

Adjust chunking in `utils/load_docs.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=750,
    chunk_overlap=150,
    separators=["\n\n", "\n", ".", " "],
)
```

## 🐛 Troubleshooting

### Redis Connection Error
- Ensure Redis is running: `redis-cli ping` should return `PONG`

### MCP Server Not Starting
- Check Node.js installation: `node --version`
- Verify MCP packages are installed globally

### Pinecone Index Error
- Ensure index named "rag" exists in your Pinecone dashboard
- Verify embeddings dimension matches (384 for MiniLM-L6-v2)

### Slow Responses
- Check Groq API rate limits
- Consider reducing `k` value in retriever settings

## 📊 Graph Visualization

The agent workflow can be visualized using the generated `graph_diagram.png`:

```
START → Router Agent → [Web Agent | Vector Agent | Geography Agent] → END
```

## 📜 License

MIT License

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 Description (Short)

```
Multi-agent RAG system with intelligent query routing using LangGraph, MCP tools integration (Tavily, Wikipedia, Airbnb), Pinecone vector store, and custom geography services. Features DeepSeek R1 router and Qwen3-32B agents.
```

## 📝 Description (GitHub About)

```
🤖 Multi-Agentic RAG with MCP Tools - Intelligent query routing, document search, web search & geography services powered by LangGraph, Groq, and Pinecone
```

## 🏷️ Topics/Tags

```
multi-agent, rag, langgraph, langchain, mcp, model-context-protocol, pinecone, groq, qwen, deepseek, fastapi, streamlit, vector-database, retrieval-augmented-generation, ai-agents
```



<img width="1867" height="841" alt="image" src="https://github.com/user-attachments/assets/30182077-adf7-444b-a68c-c4eed8c44da3" />



<img width="1791" height="818" alt="image" src="https://github.com/user-attachments/assets/1ae95bfa-56d1-4ff5-95de-acf5499a739b" />
