import asyncio
import importlib
import json
from pathlib import Path

import pytest
from langchain_core.messages import ToolMessage
from langchain_askjapan import AskJapanToolkit, MaruJapanHandsToolkit, JapanMCPError
from conftest import fake_connection

@pytest.mark.parametrize("cls,key,count", [(AskJapanToolkit,"ask",14),(MaruJapanHandsToolkit,"maru",11)])
def test_live_schema_and_individual_exports(cls,key,count):
    tools = cls(connection=fake_connection(key),tool_names=None).get_tools()
    expected = json.loads((Path(__file__).parents[1]/"fixtures"/f"{key}-tools.json").read_text())["tools"]
    assert len(tools) == count
    mod = importlib.import_module("langchain_askjapan." + ("ask_japan" if key == "ask" else "maru"))
    for actual, remote in zip(tools,expected):
        assert actual.name == remote["name"]
        assert actual.description == remote["description"]
        assert actual.args_schema == remote["inputSchema"]
        assert callable(getattr(mod,actual.name))
        assert callable(getattr(mod,"aload_"+actual.name))


def test_default_public_tools_and_unknown():
    kit=AskJapanToolkit(connection=fake_connection("ask"))
    assert len(kit.get_tools()) == 6
    with pytest.raises(ValueError, match="Unknown MCP"):
        kit.get_tool("not_a_tool")

async def test_sync_inside_loop_async_batch_and_artifact():
    tool=AskJapanToolkit(connection=fake_connection("ask")).get_tool("lookup_postcode")
    call={"type":"tool_call","id":"abc","name":tool.name,"args":{"postcode":"530-0001"}}
    sync=tool.invoke(call)
    result=await tool.ainvoke(call)
    assert isinstance(sync,ToolMessage) and isinstance(result,ToolMessage)
    assert sync.content[0]["text"] == result.content[0]["text"]
    assert result.artifact["structured_content"]["arguments"] == call["args"]
    assert len(await tool.abatch([{"postcode":"530-0001"}]*2)) == 2
    assert len(tool.batch([{"postcode":"530-0001"}]*2)) == 2

async def test_network_failure_sync_and_async():
    kit=AskJapanToolkit(connection={"transport":"http","url":"http://127.0.0.1:1/mcp","timeout":0.2})
    with pytest.raises(JapanMCPError, match="无法读取"):
        kit.get_tools()
    with pytest.raises(JapanMCPError, match="Cannot discover"):
        await kit.aget_tools()

async def test_server_error_preserved():
    tool=await AskJapanToolkit(connection=fake_connection("ask")).aget_tool("search_company")
    result=await tool.ainvoke({"type":"tool_call","id":"err","name":tool.name,"args":{"name":"ERROR"}})
    assert result.status == "error"
    assert "Fake service error" in str(result.content)

async def test_cancellation_propagates():
    tool=await AskJapanToolkit(connection=fake_connection("ask")).aget_tool("search_company")
    task=asyncio.create_task(tool.ainvoke({"name":"SLOW"}))
    await asyncio.sleep(0.2)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


def test_import_does_not_connect(monkeypatch):
    from langchain_mcp_adapters.client import MultiServerMCPClient
    def fail(*a,**kw): raise AssertionError("network on import")
    monkeypatch.setattr(MultiServerMCPClient,"get_tools",fail)
    import langchain_askjapan.ask_japan as mod
    importlib.reload(mod)
    AskJapanToolkit()

async def test_invocation_connection_error_bilingual():
    from langchain_core.tools import StructuredTool
    from langchain_askjapan._base import bridge
    async def unavailable(**kwargs):
        raise ConnectionError("private upstream detail")
    tool=bridge(StructuredTool(name="network_test",description="local transport failure",args_schema={"type":"object","properties":{}},coroutine=unavailable))
    for method in ("sync","async"):
        with pytest.raises(JapanMCPError, match="network/session") as error:
            if method == "sync": tool.invoke({})
            else: await tool.ainvoke({})
        assert "未自动重试" in str(error.value)
        assert "private upstream detail" not in str(error.value)
        assert isinstance(error.value.__cause__,ConnectionError)
