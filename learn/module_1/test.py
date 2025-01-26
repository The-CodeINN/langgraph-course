import asyncio
from langgraph_sdk import get_client
from langchain_core.messages import HumanMessage

URL = "http://127.0.0.1:2024"
client = get_client(url=URL)


async def run_calculation(prompt: str):
    try:
        # Create thread
        thread = await client.threads.create()
        thread_id = thread["thread_id"]

        # Get assistant
        assistants = await client.assistants.search()
        assistant_id = assistants[0]["assistant_id"]

        # Create and wait for run
        result = await client.runs.wait(
            thread_id=thread_id,
            assistant_id=assistant_id,
            input={"messages": [HumanMessage(content=prompt, name="user")]},
        )

        # Print results
        if isinstance(result, dict) and "messages" in result:
            for message in result["messages"]:
                if hasattr(message, "content"):
                    print(f"Response: {message.content}")
                else:
                    print(f"Message: {message}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    asyncio.run(run_calculation("Add 3 to 4"))
