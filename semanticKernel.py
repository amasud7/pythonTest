import asyncio
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from dotenv import load_dotenv
import os
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
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

    # Use ChatHistory for conversation history

    chat_history = ChatHistory()
    chat_history.add_message(ChatMessageContent(role=AuthorRole.SYSTEM, content="You are helpful assistant that provides concise but accessible responses."))
    # history = ChatHistory()
    # history.add_system_message("You are a helpful assistant. Please answer the user's questions.")
    print("Hello! Please enter a question: ")

    while True:
        user_input = input()
        if user_input.lower() == "exit":
            break

            # get the user's message and add it to the chat history
        chat_history.add_message(ChatMessageContent(role=AuthorRole.USER, content=user_input))

        # send chat the entire history to the agent + get the agent response
        agent_response = await agent.get_response(messages=chat_history)

        # extract the text from the agent's response
        response_text = getattr(agent_response.content, "content", str(agent_response.content))

        # now, add the assistant's response to chat history
        chat_history.add_message(ChatMessageContent(role=AuthorRole.ASSISTANT, content=response_text))

        # # Add user message to ChatHistory
        # history.add_user_message(user_input)

        # # Get the response from the agent, passing the ChatHistory
        # agent_response = await agent.get_response(messages=history)
        print("AI Agent: ", agent_response.content)

        # # Add agent response to ChatHistory
        # history.add_assistant_message(agent_response.content)

   

asyncio.run(main())




