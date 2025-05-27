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

    # adding option to pick chat instructions and customize the agent
    print("Please enter chat instructions for the agent (Enter for default agent): ")
    instructions = input()
    if not instructions.strip():
        instructions = "You are a helpful assistant. Answer the user's questions to the best of your ability."


    # Initialize a chat agent with basic instructions
    agent = ChatCompletionAgent(
        service=chat_service, # pass the chat service to the agent
        name="SK-Assistant",
        instructions=instructions, # user provided instructions
    )


    history = []
    history.append(instructions)
    print("Hello! Please enter a question: ")

    while True:
        # get the user input
        user_input = input()
        # check if the user wants to exit
        if user_input.lower() == "exit":
            break

        # Add user message to history
        history.append(user_input)

        # Get the response from the agent, passing the full history
        agent_response = await agent.get_response(messages=history)
        print("AI Agent: ", agent_response.content)

        # Add agent response to history
        history.append(agent_response.content)

   

asyncio.run(main()) 



