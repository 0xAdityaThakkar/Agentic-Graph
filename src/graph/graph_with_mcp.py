from src.state.state import State
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from src.language_agents.ollama_openai import call_ollama
from src.nodes.mcp.mcp_client import MCPClient
from src.app_conf import AVAILABLE_MCP_TOOLS
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

async def discover_mcp_tools():
    tools = []
    for mcp_tool_config in AVAILABLE_MCP_TOOLS:
        client = MCPClient(
            name=mcp_tool_config["name"],
            base_url=mcp_tool_config["base_url"],
            headers=mcp_tool_config.get("headers", {}),
            timeout=mcp_tool_config.get("timeout", 5.0)
        )
        tool = await client.get_tools(mcp_tool_config.get("tools_endpoint", "/list-tools"))
        tools.append(tool)
    return tools

async def build_and_execute_graph(user_input: str):
    mcp_tools = await discover_mcp_tools()
    builder = StateGraph(State({'tools': mcp_tools}))
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
