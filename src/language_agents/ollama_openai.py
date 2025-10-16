from src.data.ollama_openai_prompt import agent_prompt_bundle
from langchain_openai import ChatOpenAI
from src.nodes.mcp.mcp_client import MCPClient

llm = ChatOpenAI(
    api_key="ollama",
    model="llama3",
    base_url="http://192.168.0.104:5050/v1",
)


async def call_ollama(state):
    try:
        prompt = state["messages"][-1]["content"]
        response = await llm.ainvoke(prompt)
        state["messages"].append({"role": "assistant", "content": response})
        return state
    except Exception as e:
        state["messages"].append({"role": "assistant", "content": "Call mcp: tool"})
        return state

async def build_ollama_prompt(mcp_tools):
    pass
