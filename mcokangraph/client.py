from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent


import asyncio


async def main():
    client = MultiServerMCPClient(
        {
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )
    llm = ChatGroq(model="llama3-8b-8192")
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools=tools)
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What is the weather in Tokyo?"}]}
    )
    print(response)


asyncio.run(main())
