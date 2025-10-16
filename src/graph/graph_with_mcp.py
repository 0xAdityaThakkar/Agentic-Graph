from src.state.state import State
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from src.language_agents.ollama_openai import call_ollama
from src.nodes.mcp_tool import mcp_node as mcp_tool_node

def router_node(state: State):
    # node handlers must return a state dict (no-op router)
    return state

def router_decision(state: State) -> str:
    # decision function returns the next node id
    messages = state.get("messages", [])
    if not messages:
        return "return_response"
    last = messages[-1]
    if isinstance(last, dict):
        content = last.get("content", "") or last.get("text", "")
    else:
        content = getattr(last, "content", None) or getattr(last, "text", None) or str(last)
    if "mcp:" in content:
        return "mcp_tool"
    return "return_response"

def return_response(state):
    return state

async def build_and_execute_graph(user_input: str):
    builder = StateGraph(State)
    builder.add_node("llm", call_ollama)
    builder.add_node("router", router_node)
    builder.add_node("mcp_tool", mcp_tool_node)
    builder.add_node("return_response", return_response)

    builder.set_entry_point("llm")
    builder.add_edge("llm", "router")
    builder.add_conditional_edges("router", router_decision, {
        "mcp_tool": "mcp_tool",
        "return_response": "return_response",
    })
    builder.add_edge("mcp_tool", END)
    builder.add_edge("return_response", END)

    graph = builder.compile()
    return await graph.ainvoke({"messages": [{"role": "user", "content": user_input}]})
