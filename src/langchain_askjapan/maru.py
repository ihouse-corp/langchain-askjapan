"""Individually importable factories; live metadata, no network on import."""
from typing import Any
from langchain_core.tools import BaseTool
from .toolkits import MaruJapanHandsToolkit


def list_services(**config: Any) -> BaseTool:
    """Load the live ``list_services`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("list_services")

async def aload_list_services(**config: Any) -> BaseTool:
    """Asynchronously load the live ``list_services`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("list_services")


def check_availability(**config: Any) -> BaseTool:
    """Load the live ``check_availability`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("check_availability")

async def aload_check_availability(**config: Any) -> BaseTool:
    """Asynchronously load the live ``check_availability`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("check_availability")


def request_service(**config: Any) -> BaseTool:
    """Load the live ``request_service`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("request_service")

async def aload_request_service(**config: Any) -> BaseTool:
    """Asynchronously load the live ``request_service`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("request_service")


def get_request_status(**config: Any) -> BaseTool:
    """Load the live ``get_request_status`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("get_request_status")

async def aload_get_request_status(**config: Any) -> BaseTool:
    """Asynchronously load the live ``get_request_status`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("get_request_status")


def quote_purchase(**config: Any) -> BaseTool:
    """Load the live ``quote_purchase`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("quote_purchase")

async def aload_quote_purchase(**config: Any) -> BaseTool:
    """Asynchronously load the live ``quote_purchase`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("quote_purchase")


def get_menu(**config: Any) -> BaseTool:
    """Load the live ``get_menu`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("get_menu")

async def aload_get_menu(**config: Any) -> BaseTool:
    """Asynchronously load the live ``get_menu`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("get_menu")


def check_open(**config: Any) -> BaseTool:
    """Load the live ``check_open`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("check_open")

async def aload_check_open(**config: Any) -> BaseTool:
    """Asynchronously load the live ``check_open`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("check_open")


def place_takeout_order(**config: Any) -> BaseTool:
    """Load the live ``place_takeout_order`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("place_takeout_order")

async def aload_place_takeout_order(**config: Any) -> BaseTool:
    """Asynchronously load the live ``place_takeout_order`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("place_takeout_order")


def maru_wallet_connect(**config: Any) -> BaseTool:
    """Load the live ``maru_wallet_connect`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("maru_wallet_connect")

async def aload_maru_wallet_connect(**config: Any) -> BaseTool:
    """Asynchronously load the live ``maru_wallet_connect`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("maru_wallet_connect")


def maru_wallet_request_payment(**config: Any) -> BaseTool:
    """Load the live ``maru_wallet_request_payment`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("maru_wallet_request_payment")

async def aload_maru_wallet_request_payment(**config: Any) -> BaseTool:
    """Asynchronously load the live ``maru_wallet_request_payment`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("maru_wallet_request_payment")


def maru_wallet_request_status(**config: Any) -> BaseTool:
    """Load the live ``maru_wallet_request_status`` tool. Invoke with its original MCP arguments."""
    return MaruJapanHandsToolkit(**config).get_tool("maru_wallet_request_status")

async def aload_maru_wallet_request_status(**config: Any) -> BaseTool:
    """Asynchronously load the live ``maru_wallet_request_status`` tool."""
    return await MaruJapanHandsToolkit(**config).aget_tool("maru_wallet_request_status")

