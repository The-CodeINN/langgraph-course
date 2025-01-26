from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    RemoveMessage,
    SystemMessage,
    trim_messages,
)
from pprint import pprint

from learn.config import config

model = ChatOpenAI(api_key=config.openai_api_key, model="gpt-4o-mini", temperature=0)


class State(MessagesState):
    summary: str = ""


def summarize(state: State) -> dict:
    summary = state.get("summary", "")

    # if there is summary, we add it
    if summary:
        sys_msg = f"Summary of the conversation ealier: {summary}"
        # add summary to system message
        messages = [SystemMessage(content=sys_msg)] + state["messages"]

    else:
        messages = state["messages"]

    response = model.invoke(messages)
    return {"messages": response}


def summarize_conversation(state: State) -> dict:
    summary = state.get("summary", "")

    # if there is summary, we add it
    if summary:
        summary_msg = (
            f"This is the summary of the conversation to date: {summary}\n\n"
            "Extend the summry by taking into account the new message above:"
        )

    else:
        summary_msg = "Create a summary of the conversation to above:"

    messages = state["messages"] + [
        HumanMessage(content=summary_msg, name="user", id="1")
    ]
    response = model.invoke(messages)

    # delete all but 2 most recent messages
    delete_messages = [RemoveMessage(id=msg.id) for msg in messages[:-2]]
    return {"summary": response.content, "messages": delete_messages}


def should_continue(state: State) -> str:
    messages = state["messages"]

    # if there are more than 5 messages, we should summarize
    if len(messages) > 5:
        return "summarize_conversation"

    return END


workflow = StateGraph(State)
workflow.add_node("summarize", summarize)
workflow.add_node("summarize_conversation", summarize_conversation)

workflow.add_edge(START, "summarize")
workflow.add_conditional_edges("summarize", should_continue)
workflow.add_edge("summarize_conversation", END)

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
