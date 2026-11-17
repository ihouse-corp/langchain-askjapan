"""A real MCP stdio server, fully local; never forwards production requests."""
import asyncio
import json
from pathlib import Path
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

server = Server("fake-japan")
tools = [Tool.model_validate(t) for t in json.loads(
    (Path(__file__).parent / "fixtures" / f"{sys.argv[1]}-tools.json").read_text()
)["tools"]]

@server.list_tools()
async def listing():
    return tools

@server.call_tool()
async def call(name, arguments):
    if arguments.get("name") == "ERROR":
        return CallToolResult(isError=True, content=[TextContent(type="text", text="Fake service error")])
    if arguments.get("name") == "SLOW":
        await asyncio.sleep(60)
    payload = {"fake": True, "name": name, "arguments": arguments}
    return CallToolResult(content=[TextContent(type="text", text=json.dumps(payload))], structuredContent=payload)

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

asyncio.run(main())
