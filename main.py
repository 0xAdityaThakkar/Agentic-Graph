# main.py
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from src.controller import routes
from src.nodes.mcp.mcp_registry import build_mcp_registry
from src.language_agents.ollama_openai import build_ollama_prompt

@asynccontextmanager
async def lifespan(app: FastAPI):
    mcp_tools = await build_mcp_registry()
    network_agent_llm_prompt = await build_ollama_prompt(mcp_tools)
    app.state.mcp_tools = mcp_tools
    app.state.llm_prompt = network_agent_llm_prompt
    yield
    # Code after yield will run on shutdown
    print("Application is shutting down.")

load_dotenv()
app = FastAPI(lifespan=lifespan)

# Include the router from the items module
app.include_router(routes.router)
