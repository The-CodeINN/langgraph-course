from learn.config import config

from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

messages = [
    AIMessage(content="Hello, I am a bot.", name="bot"),
]

messages.extend([HumanMessage(content="Hi bot, can you tell me a joke?", name="user")])
messages.extend(
    [
        AIMessage(
            content="Sure, here is a joke: Why did the scarecrow win an award? Because he was outstanding in his field.",
            name="bot",
        )
    ]
)


llm = ChatOpenAI(api_key=config.openai_api_key, model="gpt-4o-mini")
# result = llm.invoke(messages)


def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together.

    Args:
        a: The first number.
        b: The second number.
    """
    return a * b


llm_with_tools = llm.bind_tools([multiply])

tool_call = llm_with_tools.invoke(
    [HumanMessage(content="What is 5 times 5?", name="user")]
)

initial_messages = [
    HumanMessage(content="What is 5 times 5?", name="user"),
    AIMessage(content="25", name="bot"),
]

new_messages = AIMessage(content="25", name="bot")
test = add_messages(initial_messages, new_messages)
print(test)
