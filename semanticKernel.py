import asyncio
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from dotenv import load_dotenv
import os
from semantic_kernel.contents import ChatHistory
load_dotenv()

# trying ChatHistory for conversation history

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
BASEURL = os.getenv("AZURE_OPENAI_ENDPOINT")
CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

async def main():
    # pass credentials to the AzureChatCompletion
    chat_service = AzureChatCompletion(
        endpoint=BASEURL,
        api_key=API_KEY,
        deployment_name=CHAT_DEPLOYMENT_NAME,
    )

    # Initialize a chat agent with basic instructions
    agent = ChatCompletionAgent(
        service=chat_service, # pass the chat service to the agent
        name="SK-Assistant",
        instructions="You are a helpful assistant.",
    )

    # Use ChatHistory for conversation history
    history = ChatHistory()
    history.add_system_message("You are a helpful assistant. Please answer the user's questions.")
    print("Hello! Please enter a question: ")

    while True:
        user_input = input()
        if user_input.lower() == "exit":
            break

        # Add user message to ChatHistory
        history.add_user_message(user_input)

        # Get the response from the agent, passing the ChatHistory
        agent_response = await agent.get_response(messages=history)
        print("AI Agent: ", agent_response.content)

        # Add agent response to ChatHistory
        history.add_assistant_message(agent_response.content)

   

asyncio.run(main())




