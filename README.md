(The file `/Users/aditya/ai_playground/agentic-graph/README.md` exists, but is empty)
# Agentic-Graph

Lightweight experiment wiring a small LangGraph-like workflow to a locally
hosted Ollama model and a FastAPI HTTP interface.

This repository contains:

- `src/router/routes.py` — FastAPI router exposing two endpoints:
	- `POST /generate` — proxies a prompt to a local Ollama server and returns the generated text
	- `POST /run_graph` — creates the project graph via `create_langgraph()` and invokes it
- `src/graph/graph.py` — graph builder (creates nodes for LLM + tool stubs)
- `src/state/state.py` — a small TypedDict state schema used by the graph

Goals and assumptions
- The project is a minimal prototype. Tool nodes (API, DB, RAG, MCP, email)
	are currently lightweight placeholders; replace them with real integrations when ready.
- A locally-hosted Ollama server is expected to be available at `http://localhost:11434/api/generate`.
	You can configure the URL inside `src/router/routes.py` or replace the call with your preferred client.

Quickstart

1. Create a virtual environment and install requirements (you may already have FastAPI installed):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or: pip install fastapi uvicorn
```

2. Run the FastAPI app (example using uvicorn):

```bash
uvicorn main:app --reload --port 8000
```

3. Test the endpoints

- POST /generate

Request body:

```json
{ "prompt": "Hello from Agentic-Graph", "model": "llama3" }
```

Response:

```json
{ "model": "llama3", "text": "...generated text..." }
```

- POST /run_graph

Request body (optional):

```json
{ "input": { "messages": [{"role":"user","content":"Hello"}] } }
```

Response (varies depending on graph implementation):

```json
{ "method": "invoke", "result": { ... } }
```

Notes and next steps
- If your Ollama server runs on a different host/port, update the URL in `src/router/routes.py` or provide an environment-based configuration.
- Replace the tool stub nodes in `src/graph/graph.py` with real implementations for API calls, database queries, RAG retrieval, MCP handling, and email sending.
- Consider adding tests under `tests/` to validate graph execution and endpoint behavior.

If you want, I can now implement the `create_langgraph()` function (or a Langgraph class) so `/run_graph` has a runnable graph with LLM + tool nodes. Tell me whether you prefer realistic tool implementations or simple stubs.

