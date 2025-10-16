# mcp_manager.py
import asyncio
import logging
from typing import Dict, Callable, Any
from src.nodes.mcp.mcp_client import MCPClient

logger = logging.getLogger("MCPManager")

class MCPClientManager:
    def __init__(self):
        self.clients: Dict[str, MCPClient] = {}
        self.routing_strategy: Callable[[Dict[str, Any]], str] = lambda payload: list(self.clients.keys())[0]

    def register_client(self, client: MCPClient):
        self.clients[client.name] = client
        logger.info(f"Registered MCP client: {client.name}")

    def set_routing_strategy(self, strategy: Callable[[Dict[str, Any]], str]):
        self.routing_strategy = strategy

    async def send(self, endpoint: str, payload: Dict[str, Any], retries: int = 2) -> Dict[str, Any]:
        client_name = self.routing_strategy(payload)
        client = self.clients.get(client_name)
        if not client:
            raise ValueError(f"No client named '{client_name}'")

        for attempt in range(retries + 1):
            try:
                logger.info(f"Sending to {client_name}, attempt {attempt + 1}")
                return await client.send(endpoint, payload)
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(0.5 * (attempt + 1))
        raise RuntimeError(f"All retries failed for client '{client_name}'")

    async def broadcast(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for name, client in self.clients.items():
            try:
                results[name] = await client.send(endpoint, payload)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results

    async def health_report(self) -> Dict[str, bool]:
        return {name: await client.health_check() for name, client in self.clients.items()}
