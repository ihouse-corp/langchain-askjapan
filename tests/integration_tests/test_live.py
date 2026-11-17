"""Explicitly opt-in free, read-only production standard tests."""
import os
import pytest
from langchain_tests.integration_tests.tools import ToolsIntegrationTests
from langchain_askjapan.ask_japan import lookup_postcode, search_company
from langchain_askjapan.maru import list_services

pytestmark=[pytest.mark.live,pytest.mark.skipif(os.getenv("ASKJAPAN_LIVE_TESTS")!="1",reason="Requires explicit free read-only live test opt-in")]

class TestPostcode(ToolsIntegrationTests):
    @property
    def tool_constructor(self): return lookup_postcode
    @property
    def tool_invoke_params_example(self): return {"postcode":"530-0001"}

class TestCompany(ToolsIntegrationTests):
    @property
    def tool_constructor(self): return search_company
    @property
    def tool_invoke_params_example(self): return {"name":"トヨタ自動車","limit":1}

class TestServices(ToolsIntegrationTests):
    @property
    def tool_constructor(self): return list_services
    @property
    def tool_invoke_params_example(self): return {}
