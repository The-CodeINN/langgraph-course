from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState


class State(TypedDict):
    graph_state: str


class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class BuiltState(MessagesState):
    pass
