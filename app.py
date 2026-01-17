import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent,MCPClient

async def run_memory_chat():
    load_dotenv()
    os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')


    config_file = 'browser_mcp.json'

    print("Initailizing chat....")

    client = MCPClient(config_file)
    llm = ChatGroq(model='llama-3.3-70b-versatile',tool_choice='none')

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=5,
        memory_enabled=True,
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the chat.")
    print("Type 'clear' to clear the memory.")
    print("================================\n")


    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ['exit', 'quit']:
                print("Ending chat...")
                break
            
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print('Conversation history cleared.')
                continue

            print("\nAssistant: ",end="",flush=True)

            try:
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:

        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())