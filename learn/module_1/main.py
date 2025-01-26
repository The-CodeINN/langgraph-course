from learn.config import config
from pprint import pprint

from langgraph.graph import StateGraph, START, END
from learn.module_1.state import State, BuiltState
from learn.module_1.nodes import (
    node_1,
    node_2,
    node_3,
    decide_mood,
    tool_calling_node,
    multiply,
)

from learn.module_1.tools import tools

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver


llm = ChatOpenAI(api_key=config.openai_api_key, model="gpt-4o-mini")

llm_with_tools = llm.bind_tools(tools)

prompts = SystemMessage(
    content="You are a helpful assistant task with performing arithmetic calculations on a set of inputs",
    name="bot",
)


# assistant node
def assistant_node(state: BuiltState):
    messages = llm_with_tools.invoke([prompts] + state["messages"])
    if not isinstance(messages, list):
        messages = [messages]
    return {"messages": messages}


builder = StateGraph(BuiltState)

builder.add_node("assistant_node", assistant_node)
builder.add_node("tools", ToolNode(tools))

# edges
builder.add_edge(START, "assistant_node")
builder.add_conditional_edges("assistant_node", tools_condition)
builder.add_edge("tools", "assistant_node")
builder.add_edge("assistant_node", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# messages = graph.invoke({"messages": HumanMessage(content="Hi", name="user")})

# config = {"configurable": {"thread_id": "1"}}

# messages_2 = graph.invoke(
#     {
#         "messages": HumanMessage(
#             content="What is the square of 4, add it to 6", name="user"
#         )
#     },
#     config=config,
# )

# message_3 = graph.invoke(
#     {"messages": HumanMessage(content="Subtract that from 4", name="user")},
#     config=config,
# )

# # print(messages)
# for message in messages_2["messages"]:
#     message.pretty_print()

# for message in message_3["messages"]:
#     message.pretty_print()
