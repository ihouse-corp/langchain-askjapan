"""Official tool suites for every registered tool, backed only by fake MCP."""
import json
from pathlib import Path
from langchain_mcp_adapters.tools import convert_mcp_tool_to_langchain_tool
from langchain_tests.unit_tests.tools import ToolsUnitTests
from langchain_tests.integration_tests.tools import ToolsIntegrationTests
from mcp.types import Tool
from langchain_askjapan._base import bridge
from conftest import fake_connection


def example(schema):
    if "enum" in schema: return schema["enum"][0]
    kind=schema.get("type")
    if kind == "object": return {k:example(schema["properties"][k]) for k in schema.get("required",[])}
    if kind == "array": return [example(schema["items"])]*schema.get("minItems",1)
    if kind == "string": return "x"*max(13,schema.get("minLength",0))
    if kind in ("integer","number"): return schema.get("minimum",1)
    if kind == "boolean": return False
    return None


def suite(key,raw,base):
    def constructor(**kwargs):
        return bridge(convert_mcp_tool_to_langchain_tool(None,Tool.model_validate(raw),connection=fake_connection(key)))
    return type("Test_"+base.__name__+"_"+key+"_"+raw["name"],(base,),{
        "tool_constructor":property(lambda self:constructor),
        "tool_constructor_params":property(lambda self:{}),
        "tool_invoke_params_example":property(lambda self:example(raw["inputSchema"])),
    })

for key in ("ask","maru"):
    for raw in json.loads((Path(__file__).parents[1]/"fixtures"/f"{key}-tools.json").read_text())["tools"]:
        for base in (ToolsUnitTests,ToolsIntegrationTests):
            cls=suite(key,raw,base)
            globals()[cls.__name__]=cls
del cls
