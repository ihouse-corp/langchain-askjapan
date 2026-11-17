"""Live MCP discovery and synchronous/asynchronous LangChain bridging."""
from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from typing import Any, Callable, Coroutine, TypeVar

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool, ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import Field

T = TypeVar("T")


class JapanMCPError(ToolException):
    """Bilingual, credential-free connection/session failure."""


def run_sync(factory: Callable[[], Coroutine[Any, Any, T]]) -> T:
    """Run without a persistent loop/thread; supports notebook event loops too."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(factory())
    context = copy_context()
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(context.run, lambda: asyncio.run(factory())).result()


def bridge(tool: BaseTool) -> BaseTool:
    """Keep the official adapter tool, schema, artifacts and error semantics."""
    if not isinstance(tool, StructuredTool) or tool.coroutine is None:
        raise TypeError("Expected an async MCP StructuredTool / 需要异步 MCP 工具")
    original = tool.coroutine

    async def invoke(**kwargs: Any) -> Any:
        try:
            return await original(**kwargs)
        except ToolException:
            raise
        except Exception as exc:
            if (task := asyncio.current_task()) is not None and task.cancelling():
                raise asyncio.CancelledError() from exc
            # Do not include response bodies, arguments, URLs or credentials.
            raise JapanMCPError(
                f"MCP tool {tool.name} failed: network/session or response error. "
                "Check connectivity and service availability; no automatic retry. "
                "MCP 工具调用失败：网络、会话或响应异常；请检查连接及服务状态。"
                "未自动重试；有副作用的请求请先确认状态，避免重复执行。"
            ) from exc

    tool.coroutine = invoke
    tool.func = lambda **kwargs: run_sync(lambda: invoke(**kwargs))
    return tool


class MCPToolkit(BaseToolkit):
    """Discover tools on each load; construction and imports perform no I/O.

    ``connection`` accepts an official adapter connection configuration for
    private gateways or isolated tests. Never expose credentials in traces.
    ``tool_names`` controls which tools are returned, not server permissions.
    """

    endpoint: str
    server_name: str
    tool_names: tuple[str, ...] | None = None
    timeout: float = Field(default=30.0, gt=0)
    connection: dict[str, Any] | None = Field(default=None, exclude=True, repr=False)

    async def aget_tools(self) -> list[BaseTool]:
        connection = self.connection or {
            "transport": "http", "url": self.endpoint,
            "timeout": self.timeout, "sse_read_timeout": self.timeout,
        }
        try:
            tools = await MultiServerMCPClient(
                {self.server_name: connection}
            ).get_tools(server_name=self.server_name)
        except Exception as exc:
            if (task := asyncio.current_task()) is not None and task.cancelling():
                raise asyncio.CancelledError() from exc
            raise JapanMCPError(
                "Cannot discover MCP tools. Check connectivity, endpoint and credentials. "
                "无法读取 MCP 工具清单，请检查网络、端点和凭据。"
            ) from exc
        if self.tool_names is not None:
            available = {t.name for t in tools}
            missing = set(self.tool_names) - available
            if missing:
                raise ValueError(f"Unknown MCP tools / 线上无此工具: {sorted(missing)}")
            tools = [t for t in tools if t.name in self.tool_names]
        return [bridge(t) for t in tools]

    def get_tools(self) -> list[BaseTool]:
        return run_sync(self.aget_tools)

    async def aget_tool(self, name: str) -> BaseTool:
        """Load one named tool, even if excluded from this toolkit's default list."""
        toolkit = self.model_copy(update={"tool_names": (name,)})
        return (await toolkit.aget_tools())[0]

    def get_tool(self, name: str) -> BaseTool:
        return run_sync(lambda: self.aget_tool(name))
