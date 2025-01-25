from learn.config import config

from langgraph.graph import StateGraph, START, END
from learn.module_1.state import State, BuiltState
from learn.module_1.nodes import node_1, node_2, node_3, decide_mood, tool_calling_node
from langchain_core.messages import HumanMessage

builder = StateGraph(BuiltState)

# builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
# builder.add_node("node_3", node_3)

# builder.add_edge(START, "node_1")
# builder.add_conditional_edges("node_1", decide_mood)
# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)

builder.add_node("tool_calling_node", tool_calling_node)
builder.add_edge(START, "tool_calling_node")
builder.add_edge("tool_calling_node", END)

graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content="Hi", name="user")})

messages_2 = graph.invoke(
    {"messages": HumanMessage(content="What is 5 times 5?", name="user")}
)

# print(messages)
print(messages_2)
