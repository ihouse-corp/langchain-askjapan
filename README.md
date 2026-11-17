# langchain-askjapan

LangChain Python tools for **Ask Japan** public data and **MARU Japan Hands** human services in Japan, operated by iHouse Co., Ltd.

Version 0.1.0 is published on PyPI.
Python 3.11+; validated locally on Python 3.12. No LLM subscription is needed to run the direct examples.

## Overview

| Class | Default tools | Sync / async | Serializable | JavaScript |
| --- | --- | --- | --- | --- |
| `AskJapanToolkit` | Six public-data tools | Yes / yes | No | Not provided |
| `MaruJapanHandsToolkit` | All 11 MARU tools | Yes / yes | No | Not provided |

Built on the official `langchain-mcp-adapters`. Tool **names, descriptions, JSON input schemas and annotations come from live MCP discovery**, without renaming or manually recreating arguments. The adapter's content blocks, structured artifacts and MCP execution errors are preserved. Construction/import is offline; loading a tool and each invocation require a network connection. Each invocation opens and closes an independent MCP session; no persistent background process or automatic retries.

Endpoints are taken from the Official MCP Registry, not inferred:

- Ask Japan: `https://askjapan.senpinai.com/mcp` (`com.senpinai/ask-japan`). Its 14 tools include eight human-service/restaurant tools; the toolkit defaults to the six public-data tools.
- MARU: `https://maru.senpinai.com/mcp` (`io.github.ihouse-corp/maru-japan-hands`). Its 11 tools include three wallet tools.

## Installation

Install the published package from PyPI:

```bash
python -m pip install langchain-askjapan
```

Connecting, listing tools and the three examples below require no account or API key. Private gateways may be configured using the official adapter's `connection` mapping. Never include wallet tokens in logs or enable external tracing for sensitive calls without authorization.

## Three minimal examples

### Search Japanese companies (free, read-only)

```python
from langchain_askjapan.ask_japan import search_company

tool = search_company()
print(tool.invoke({"name": "トヨタ自動車", "limit": 1}))
```

Name search is a partial match; the first result is not guaranteed to be Toyota Motor Corporation itself. Use the corporate number when you need an exact legal entity.

### Look up a postcode (free, read-only)

```python
from langchain_askjapan.ask_japan import lookup_postcode

tool = lookup_postcode()
print(tool.invoke({"postcode": "530-0001"}))
```

### Read MARU's service catalogue (free information; services are paid)

```python
import asyncio
from langchain_askjapan.maru import aload_list_services

async def main():
    tool = await aload_list_services()
    print(await tool.ainvoke({}))

asyncio.run(main())
```

In a notebook with a running event loop, use `await main()` instead of `asyncio.run(main())`.
The runnable `examples/read_only.py` contains these three calls.

## Toolkits and individual tools

```python
from langchain_askjapan import AskJapanToolkit, MaruJapanHandsToolkit

public_tools = AskJapanToolkit().get_tools()
service_catalogue = MaruJapanHandsToolkit(tool_names=("list_services",)).get_tools()
```

Every registered tool has an independently importable synchronous factory named exactly after the MCP tool in `langchain_askjapan.ask_japan` or `langchain_askjapan.maru`. Each also has an `aload_<tool_name>` asynchronous factory. The resulting `BaseTool` supports both `.invoke(args)` and `.ainvoke(args)`, as well as standard LangChain batching and ToolCalls.

`toolkit.get_tool(name)` / `await toolkit.aget_tool(name)` explicitly load one tool even if it is outside the toolkit's default subset. `tool_names=None` loads all tools on that endpoint, including side-effectful ones. `tool_names` is a selection mechanism, not an authorization boundary. Unknown or removed tools raise a clear error; the package never silently falls back to stale bundled schemas.

### As a ToolCall

```python
from langchain_askjapan.ask_japan import lookup_postcode

tool = lookup_postcode()
message = tool.invoke({
    "type": "tool_call", "id": "postcode-1", "name": tool.name,
    "args": {"postcode": "530-0001"},
})
print(message.content)
```

### Within an agent

Illustrative composition only; not part of the no-cost test run. Supply your own configured tool-calling model. Model-provider charges are separate.

```python
# Requires the separate langchain package and a configured model.
from langchain.agents import create_agent
from langchain_askjapan import AskJapanToolkit

# model = your_existing_tool_calling_model
# agent = create_agent(model=model, tools=AskJapanToolkit().get_tools())
```

Only pass explicitly approved tools to agents. Loading a tool does not authorize a purchase, service request, wallet pairing or payment request.

## Pricing and authorization

The package itself is MIT-licensed. Hosted services follow the operator's pricing policy:

- Data that the operator obtains for free is provided free.
- Paid data is offered at market price through formal agency arrangements, plus a small handling fee for avoiding separate account registration. The exact handling fee has **not** been set; this package does not invent one.
- MARU human services are separately charged under the existing fixed-price schedule. Read `list_services` for the current schedule, limits and exclusions, and confirm the task/quote/payment separately before requesting fulfillment.

The six currently documented free public-data tools are individually listed below. This does **not** mean all current or future data products are free.

| Free public-data tool | Source |
| --- | --- |
| `search_company` | National Tax Agency corporate-number public data |
| `get_company_profile` | National Tax Agency corporate/invoice public data |
| `check_invoice` | National Tax Agency qualified-invoice publication data |
| `search_listed_companies` | Financial Services Agency EDINET code list |
| `lookup_postcode` | Japan Post postcode data |
| `search_address` | Japan Post postcode data |

`list_services` is a free read-only catalogue query, not a purchase. `check_availability`, `get_request_status`, `quote_purchase`, `get_menu` and `check_open` provide information; their returned quotes or menu prices are not charges for fulfilling a service. The examples only use `list_services` from this group.

`request_service` creates a service request. `place_takeout_order` creates an order even if payment happens later. `maru_wallet_connect` pairs an agent; `maru_wallet_request_payment` files a payment approval request. Do not use these as installation tests or without explicit authorization. `maru_wallet_request_status` requires a sensitive agent token; it is not exercised in public smoke tests. Wallet approval remains with the wallet owner; this library never approves payments.

## Errors, timeouts and operation

Network, session and response-conversion failures raise `JapanMCPError` with English and Chinese guidance. The original exception is chained for debugging; do not share full traces containing credentials. MCP application errors retain the official adapter's `ToolMessage(status="error")` behavior. There are no automatic retries, because a timeout does not prove a side-effectful request was not accepted.

`timeout=30.0` configures the default HTTP and stream-read timeouts. A custom `connection` takes precedence and must carry its own timeout settings. Sync calls block the caller; inside an existing event loop they run in a short-lived worker thread. Prefer the async API in async applications. Cancellation propagates normally on the async path.

## API reference

- `AskJapanToolkit(**config)` / `MaruJapanHandsToolkit(**config)`: `tool_names`, `timeout`, optional `endpoint`, optional official-adapter `connection`.
- `.get_tools()` / `await .aget_tools()`: discover and return selected LangChain tools.
- `.get_tool(name)` / `await .aget_tool(name)`: discover a single named tool.
- Per-tool factories: see [complete tool export inventory](docs/tool_inventory.md).
- Service documentation: [Ask Japan](https://github.com/ihouse-corp/ask-japan-mcp) and [MARU Japan Hands](https://github.com/ihouse-corp/maru-japan-hands).

## Development and verification

```bash
python -m pip install -e '.[test]' build twine
python -m pytest tests/unit_tests
# Explicitly opt in: only postcode, company search and catalogue on production.
ASKJAPAN_LIVE_TESTS=1 python -m pytest tests/integration_tests
python examples/read_only.py
python -m build
python -m twine check dist/*
```

Offline tests use a real local stdio MCP server and captured tool definitions. Official `langchain-tests==1.1.9` tool suites are applied to all 25 endpoint/tool combinations; see the local verification report for narrowly scoped incompatibility skips. No live write, order, service request, wallet operation or paid-model call is part of verification. Hosted implementation and third-party data are not licensed by this package's MIT license.

## 日本語

Ask Japan の公開データ検索と MARU Japan Hands を LangChain から使う Python パッケージです。ツール名・説明・引数は実際の MCP サーバーから取得します。現在の公開データ検索６種類とサービス一覧の参照は無料です。有料データは正式な代理条件・市場価格と少額の手数料、人的代行は既存料金表に従います。手数料の具体額は未定です。依頼・注文・ウォレット操作には別途明示的な承認が必要です。バージョン0.1.0はPyPIで公開済みです。

## 中文

这是供 LangChain 使用的 Ask Japan／MARU Python 工具包，名称、说明和参数直接取自线上 MCP。当前六个公开数据查询和服务目录查询免费；不能概括成所有数据免费。收费数据按市场价、正式代理并加少量手续费，手续费具体金额尚未定；真人代办按现有价格另算。委托、下单、钱包操作必须另获明确授权。0.1.0版已在PyPI发布。
