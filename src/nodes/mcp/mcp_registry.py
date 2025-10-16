import httpx
from src.app_conf import AVAILABLE_MCP_TOOLS

async def build_mcp_registry():
    registry = {}

    async with httpx.AsyncClient() as client:
        for server in AVAILABLE_MCP_TOOLS:
            try:
                url = f"{server['base_url']}{server['tools_endpoint']}"
                response = await client.get(url)
                tools = response.json()

                for tool in tools:
                    registry[tool["name"]] = {
                        "description": tool["description"],
                        "params": tool["params"],
                        "source": {
                            "name": server["name"],
                            "base_url": server["base_url"],
                            "run_endpoint": server["run_endpoint"]
                        }
                    }
            except Exception as e:
                print(f"Error fetching tools from {server['name']}: {e}")

    return registry

