import random
from typing import Literal
from learn.module_1.state import BuiltState
from learn.config import config

from langchain_openai import ChatOpenAI


def node_1(state):
    return {"graph_state": state["graph_state"] + "I am"}


def node_2(state):
    return {"graph_state": state["graph_state"] + " happy"}


def node_3(state):
    return {"graph_state": state["graph_state"] + " Sad"}


def decide_mood(state) -> Literal["node_2", "node_3"]:
    # Often, we will use state to decide on the next node to visit
    user_input = state["graph_state"]

    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:
        # 50% of the time, we return Node 2
        return "node_2"

    # 50% of the time, we return Node 3
    return "node_3"


def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together.

    Args:
        a: The first number.
        b: The second number.
    """
    return a * b


llm = ChatOpenAI(api_key=config.openai_api_key, model="gpt-4o-mini")

llm_with_tools = llm.bind_tools([multiply])


def tool_calling_node(state: BuiltState):
    return {"messages": llm_with_tools.invoke(state["messages"])}
