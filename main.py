import asyncio
import logging
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_default_openai_client
from agents.mcp import MCPServerStdio

logger = logging.getLogger("openai.agents.tracing")
logger.setLevel(logging.INFO)

async def main():
    custom_client = AsyncOpenAI(base_url="http://ollama.hxstarrys.me/v1")
    set_default_openai_client(custom_client)

    async with MCPServerStdio(
        params={
            "command": "kube-helper-mcp",
            "args": ["run"],
        }
    ) as mcp_server:
        tools = await mcp_server.list_tools()
        print("Tools available:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

    print("---------------------------")
    # Configure the model
    model = OpenAIChatCompletionsModel(
        model="qwen2.5:32b",
        openai_client=custom_client,
    )

    async with mcp_server:
        agent = Agent(
            name="KubeAssisstant",
            instructions="You are a helpful kubernetes assistant",
            model=model,
            mcp_servers=[mcp_server]
        )

        result = await Runner.run(agent, "List deployments in all namespaces.")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
