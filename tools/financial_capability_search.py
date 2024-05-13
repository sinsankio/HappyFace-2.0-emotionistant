from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.finance import generate_financial_capability_search_results
from utils.tools import get_description_text


class FinancialCapabilitySearchToolInput(BaseModel):
    """Input for the Financial Capability Search Tool"""

    query: str = Field(
        description="search query which consist both the exact employee id whose financial capability needs to be "
                    "looked up and their profile recommendation which is already provided to you")


class FinancialCapabilitySearchTool(BaseTool):
    """Tool that queries financial capability of an individual and gets back results"""

    name: str = "FinancialCapabilitySearchTool"
    description: str = get_description_text(name)
    args_schema: Type[BaseModel] = FinancialCapabilitySearchToolInput

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool"""
        return generate_financial_capability_search_results(query)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously"""
        return generate_financial_capability_search_results(query)
