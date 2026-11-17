"""Toolkit endpoints verified against the Official MCP Registry."""
from ._base import MCPToolkit


class AskJapanToolkit(MCPToolkit):
    """Six free Japanese public-data tools; schemas are discovered live."""
    endpoint: str = "https://askjapan.senpinai.com/mcp"
    server_name: str = "ask-japan"
    tool_names: tuple[str, ...] | None = ('search_company', 'get_company_profile', 'check_invoice', 'search_listed_companies', 'lookup_postcode', 'search_address')


class MaruJapanHandsToolkit(MCPToolkit):
    """MARU tools, including operations requiring explicit user authorization.

    Use tool_names=("list_services",) for a discovery-only agent.
    """
    endpoint: str = "https://maru.senpinai.com/mcp"
    server_name: str = "maru-japan-hands"
