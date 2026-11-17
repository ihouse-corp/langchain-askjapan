"""Free read-only examples; no LLM, requests, orders or wallet operations."""
import asyncio
import json
from langchain_askjapan.ask_japan import search_company, lookup_postcode
from langchain_askjapan.maru import aload_list_services


def main():
    results = {}
    results["search_company"] = search_company().invoke({"name": "トヨタ自動車", "limit": 1})
    results["lookup_postcode"] = lookup_postcode().invoke({"postcode": "530-0001"})

    async def services():
        tool = await aload_list_services()
        return await tool.ainvoke({})

    results["list_services"] = asyncio.run(services())
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


if __name__ == "__main__":
    main()
