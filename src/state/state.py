from typing import Annotated

from typing_extensions import TypedDict
from typing import TypedDict, Dict, Any

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    payload: Dict[str, Any]
    result: Dict[str, Any]
    tools: Dict[str, Any]


graph_builder = StateGraph(State)
