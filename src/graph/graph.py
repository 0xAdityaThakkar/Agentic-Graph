from langgraph.graph import START, END
from langchain_openai import ChatOpenAI
from src.state.state import State
from langgraph.prebuilt import tools_condition
from langchain_core.messages import AIMessage, ToolMessage

from src.nodes.push_notification import send_push_notification
from langgraph.graph import StateGraph

llm = ChatOpenAI(
    api_key="ollama",
    model="llama3",
    base_url="http://192.168.0.104:5050/v1",
)
llm_with_tools = llm.bind_tools([send_push_notification])
tools = [send_push_notification] 
# Node for calling the LLM
async def call_llm(state: State):
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}

# Node for executing tools
async def call_tool(state: State):
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    
    # Execute all pending tool calls
    outputs = await tool_executor.ainvoke(tool_calls)
    
    # Add tool outputs to the state
    return {"messages": [AIMessage(content="", tool_calls=tool_calls, tool_outputs=outputs)]}

def call_tools(state: State) -> State:
    messages = state["messages"]
    tool_calls = [msg for msg in messages if hasattr(msg, "tool_calls")]
    new_messages = messages.copy()

    for msg in tool_calls:
        for call in msg.tool_calls:
            tool_name = call["name"]
            args = call["args"]
            for tool in tools:
                if tool.name == tool_name:
                    result = tool.invoke(args)
                    new_messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return {"messages": new_messages}


def create_graph():
    builder = StateGraph(State)
    builder.add_node("call_llm", call_llm)
    builder.add_node("call_tool", call_tool)
    builder.add_edge(START, "call_llm")
    builder.add_edge("call_tool", "call_llm")
    # builder.add_node("mcp_query", mcp_node)
    builder.add_conditional_edges(
        "call_llm",
        tools_condition,
        {
            "tools": "call_tool",  # If tools are needed
            "end": END             # If no tools are needed
        }
    )
    # Compile the graph
    graph = builder.compile()
    return graph

graph = create_graph()

async def stream_graph_updates(user_input: str):
    return await graph.ainvoke({"messages": [{"role": "user", "content": user_input}]})