"""FastAPI routes for the Agentic-Graph project.

This module exposes a simple POST /generate endpoint which accepts a JSON
payload with a `prompt` (string) and an optional `model` name. The handler
forwards the prompt to a locally-hosted Ollama instance (default
http://localhost:11434/api/generate) and returns the generated text.

Note: This implementation uses only the Python standard library for the
HTTP call so there are no extra runtime dependencies required here. If you
prefer `requests` or `httpx`, feel free to swap the implementation.
"""

from __future__ import annotations


from fastapi import APIRouter, Request
from src.graph.graph import stream_graph_updates
from src.graph.graph_with_mcp import build_and_execute_graph


router = APIRouter()

@router.post("/interact")
async def interact(request: Request):
    data = await request.json()
    user_input = data['human_says']
    ai_output = await stream_graph_updates(user_input)
    return ai_output

@router.post("/interact-mcp-graph")
async def interact(request: Request):
    data = await request.json()
    user_input = data['human_says']
    ai_output = await build_and_execute_graph(user_input)
    return ai_output
