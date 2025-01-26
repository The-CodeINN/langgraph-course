from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    RemoveMessage,
    trim_messages,
)
from pprint import pprint


from learn.module_2.state import State, OverallState
from learn.module_2.tools import Tools
from learn.config import config


llm = ChatOpenAI(api_key=config.openai_api_key, model="gpt-4o-mini")

# builder = StateGraph(State)

# builder.add_node("node_1", Tools.NODE_1)
# builder.add_node("node_2", Tools.NODE_2)
# builder.add_node("node_3", Tools.NODE_3)

# builder.add_edge(START, "node_1")
# builder.add_conditional_edges("node_1", Tools.DECIDE_MOOD)
# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)

# builder = StateGraph(OverallState)
# builder.add_node("thinking_node", Tools.THINKING_NODE)
# builder.add_node("answer_node", Tools.ANSWER_NODE)
# builder.add_edge(START, "thinking_node")
# builder.add_edge("thinking_node", "answer_node")
# builder.add_edge("answer_node", END)

# graph = builder.compile()

# print(graph.invoke({"question": "hi"}))

# Initialize state with empty graph_state
# initial_state = State(name="John", mood="happy", graph_state="")
# result = graph.invoke(initial_state)


# Print final state
# print("\nFinal State:", result["graph_state"])


# initial_msg = [
#     AIMessage(content="Hi, how can i help?", name="bot", id="1"),
#     HumanMessage(content="I am feeling happy", name="user", id="2"),
# ]

# new_msg = HumanMessage(content="That's great to hear", name="user", id="2")

msg = [AIMessage(content="Hi, how can i help?", name="bot", id="1")]
msg.append(HumanMessage(content="I am feeling happy", name="user", id="2"))
msg.append(AIMessage(content="That's great to hear", name="bot", id="3"))
msg.append(HumanMessage(content="I am feeling sad", name="user", id="4"))

# for m in msg:
#     m.pretty_print()


# llm_msg = llm.invoke(msg)
# print(llm_msg)


# def chat_model_node(state: MessagesState) -> dict:
#     llm_msg = llm.invoke(state["messages"])
#     return {"messages": llm_msg}


def chat_model_node(state: MessagesState) -> dict:
    messages = trim_messages(
        state["messages"],
        max_tokens=100,
        strategy="last",
        token_counter=ChatOpenAI(model="gpt-4o"),
        allow_partial=False,
    )
    return {"messages": [llm.invoke(messages)]}


def filter_messages(state: MessagesState) -> dict:
    del_msg = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages": del_msg}


builder = StateGraph(MessagesState)

builder.add_node("chat_model_node", chat_model_node)
# builder.add_node("filter_messages", filter_messages)

builder.add_edge(START, "chat_model_node")
# builder.add_edge("filter_messages", "chat_model_node")
builder.add_edge("chat_model_node", END)

graph = builder.compile()


output = graph.invoke({"messages": msg})

msg.append(output["messages"][-1])
msg.append(HumanMessage(content="How can I be happy", name="user", id="5"))

trim_messages(
    msg,
    max_tokens=100,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    allow_partial=False,
)

messages_out_trim = graph.invoke({"messages": msg})
pprint(messages_out_trim)


# Delete all but 2 most recent messages
# del_msg = [RemoveMessage(id=m.id) for m in msg[:-2]]
# print(del_msg)

# print(add_messages(msg, del_msg))
