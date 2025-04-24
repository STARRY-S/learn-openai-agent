import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.mcp import MCPServerStdio

from agents import set_tracing_disabled
set_tracing_disabled(True)

async def main():
    custom_client = AsyncOpenAI(
        base_url="http://ollama.hxstarrys.me/v1",
        api_key="ollama"
    )
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
            instructions="You are a kubernetes assistant, "
            "you can use the data provided by MCP server to answer questions, "
            "translate the results into human readable markdown text format.",
            model=model,
            mcp_servers=[mcp_server]
        )

        result = await Runner.run(
            agent,
            input="List deployments in the `ai` namespaces.",
        )
        print("Result:")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
