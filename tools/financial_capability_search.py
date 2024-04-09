from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.finance import get_finance_capability


class FinancialCapabilitySearchToolInput(BaseModel):
    """Input for the Financial Capability Search Tool"""

    employee_id: str = Field(description="employee id of the individual whose financial capability to be looked up")


class FinancialCapabilitySearchTool(BaseTool):
    """Tool that queries financial capability of an individual and gets back results"""

    name: str = "financial_capability_search_tool"
    description: str = (
        "A search tool optimized for comprehensive, accurate, and trusted results of personal financial capabilities."
        " Useful when you need to answer questions about financial capabilities of a given individual by employee id."
        " This tool supports decision making on available loans, offers and salary deductions for an individual who"
        " currently works in the given organization."
        " Input should be an employee id."
        " Note: Always consider current date and time in any case of utilizing this tool."
    )
    args_schema: Type[BaseModel] = FinancialCapabilitySearchToolInput

    def _run(
            self,
            employee_id: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool"""
        return get_finance_capability(employee_id)

    async def _arun(
            self,
            employee_id: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool asynchronously"""
        return get_finance_capability(employee_id)
