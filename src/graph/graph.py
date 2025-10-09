from langgraph.graph import START, END
from langchain_ollama.llms import OllamaLLM
from src.state.state import graph_builder
from src.state.state import State

llm = OllamaLLM(model="llama3", base_url="http://192.168.0.104:5050")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


def create_graph():
    # The first argument is the unique node name
    # The second argument is the function or object that will be called whenever
    # the node is used.

    graph_builder.add_node("invoke_llm", chatbot)
    graph_builder.add_edge(START, "invoke_llm")
    graph_builder.add_edge("invoke_llm", END)
    graph = graph_builder.compile()

    return graph

graph = create_graph()
def stream_graph_updates(user_input: str):
    
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            return value["messages"][-1]
