import asyncio
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from dotenv import load_dotenv
import os
load_dotenv()
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

    # Get a response to a user message
    response = await agent.get_response(messages="Write a haiku about Semantic Kernel.")
    print(response.content)

asyncio.run(main()) 



