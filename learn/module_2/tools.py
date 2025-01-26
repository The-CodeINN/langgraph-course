from typing import Literal
import random
from enum import Enum
from learn.module_2.state import State, OverallState


def node_1(state: State) -> dict:
    return {"graph_state": state.graph_state + "I am"}


def node_2(state: State) -> dict:
    return {"graph_state": state.graph_state + " happy"}


def node_3(state: State) -> dict:
    return {"graph_state": state.graph_state + " sad"}


def decide_mood(state: State) -> Literal["node_2", "node_3"]:
    # Use state.mood to make decision
    if state.mood == "happy":
        return "node_2"
    elif state.mood == "sad":
        return "node_3"

    # For neutral mood, random choice
    return "node_2" if random.random() < 0.5 else "node_3"


def thinking_node(state: OverallState) -> dict:
    return {
        "answer": f"bye {state['question']}",
        "notes": f"... his name is {state['question']}",
    }


def answer_node(state: OverallState) -> dict:
    return {"notes": f"Answered {state['question']}"}


class Tools(Enum):
    NODE_1 = node_1
    NODE_2 = node_2
    NODE_3 = node_3
    DECIDE_MOOD = decide_mood
    THINKING_NODE = thinking_node
    ANSWER_NODE = answer_node
