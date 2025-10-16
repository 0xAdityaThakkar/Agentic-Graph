from src.nodes.mcp.mcp_manager import MCPClientManager
from src.state.state import State

manager = MCPClientManager()

async def mcp_node(state: State) -> State:
    result = await manager.send(endpoint="query", payload=state["payload"])
    return {"payload": state["payload"], "result": result}