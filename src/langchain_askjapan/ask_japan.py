"""Individually importable factories; live metadata, no network on import."""
from typing import Any
from langchain_core.tools import BaseTool
from .toolkits import AskJapanToolkit


def search_company(**config: Any) -> BaseTool:
    """Load the live ``search_company`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("search_company")

async def aload_search_company(**config: Any) -> BaseTool:
    """Asynchronously load the live ``search_company`` tool."""
    return await AskJapanToolkit(**config).aget_tool("search_company")


def get_company_profile(**config: Any) -> BaseTool:
    """Load the live ``get_company_profile`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("get_company_profile")

async def aload_get_company_profile(**config: Any) -> BaseTool:
    """Asynchronously load the live ``get_company_profile`` tool."""
    return await AskJapanToolkit(**config).aget_tool("get_company_profile")


def check_invoice(**config: Any) -> BaseTool:
    """Load the live ``check_invoice`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("check_invoice")

async def aload_check_invoice(**config: Any) -> BaseTool:
    """Asynchronously load the live ``check_invoice`` tool."""
    return await AskJapanToolkit(**config).aget_tool("check_invoice")


def search_listed_companies(**config: Any) -> BaseTool:
    """Load the live ``search_listed_companies`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("search_listed_companies")

async def aload_search_listed_companies(**config: Any) -> BaseTool:
    """Asynchronously load the live ``search_listed_companies`` tool."""
    return await AskJapanToolkit(**config).aget_tool("search_listed_companies")


def lookup_postcode(**config: Any) -> BaseTool:
    """Load the live ``lookup_postcode`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("lookup_postcode")

async def aload_lookup_postcode(**config: Any) -> BaseTool:
    """Asynchronously load the live ``lookup_postcode`` tool."""
    return await AskJapanToolkit(**config).aget_tool("lookup_postcode")


def search_address(**config: Any) -> BaseTool:
    """Load the live ``search_address`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("search_address")

async def aload_search_address(**config: Any) -> BaseTool:
    """Asynchronously load the live ``search_address`` tool."""
    return await AskJapanToolkit(**config).aget_tool("search_address")


def list_services(**config: Any) -> BaseTool:
    """Load the live ``list_services`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("list_services")

async def aload_list_services(**config: Any) -> BaseTool:
    """Asynchronously load the live ``list_services`` tool."""
    return await AskJapanToolkit(**config).aget_tool("list_services")


def check_availability(**config: Any) -> BaseTool:
    """Load the live ``check_availability`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("check_availability")

async def aload_check_availability(**config: Any) -> BaseTool:
    """Asynchronously load the live ``check_availability`` tool."""
    return await AskJapanToolkit(**config).aget_tool("check_availability")


def request_service(**config: Any) -> BaseTool:
    """Load the live ``request_service`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("request_service")

async def aload_request_service(**config: Any) -> BaseTool:
    """Asynchronously load the live ``request_service`` tool."""
    return await AskJapanToolkit(**config).aget_tool("request_service")


def get_request_status(**config: Any) -> BaseTool:
    """Load the live ``get_request_status`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("get_request_status")

async def aload_get_request_status(**config: Any) -> BaseTool:
    """Asynchronously load the live ``get_request_status`` tool."""
    return await AskJapanToolkit(**config).aget_tool("get_request_status")


def quote_purchase(**config: Any) -> BaseTool:
    """Load the live ``quote_purchase`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("quote_purchase")

async def aload_quote_purchase(**config: Any) -> BaseTool:
    """Asynchronously load the live ``quote_purchase`` tool."""
    return await AskJapanToolkit(**config).aget_tool("quote_purchase")


def get_menu(**config: Any) -> BaseTool:
    """Load the live ``get_menu`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("get_menu")

async def aload_get_menu(**config: Any) -> BaseTool:
    """Asynchronously load the live ``get_menu`` tool."""
    return await AskJapanToolkit(**config).aget_tool("get_menu")


def check_open(**config: Any) -> BaseTool:
    """Load the live ``check_open`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("check_open")

async def aload_check_open(**config: Any) -> BaseTool:
    """Asynchronously load the live ``check_open`` tool."""
    return await AskJapanToolkit(**config).aget_tool("check_open")


def place_takeout_order(**config: Any) -> BaseTool:
    """Load the live ``place_takeout_order`` tool. Invoke with its original MCP arguments."""
    return AskJapanToolkit(**config).get_tool("place_takeout_order")

async def aload_place_takeout_order(**config: Any) -> BaseTool:
    """Asynchronously load the live ``place_takeout_order`` tool."""
    return await AskJapanToolkit(**config).aget_tool("place_takeout_order")

