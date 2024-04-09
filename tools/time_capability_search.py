from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.time import get_time_capability


class TimeCapabilitySearchToolInput(BaseModel):
    """Input for the Time Capability Search Tool"""

    employee_id: str = Field(description="employee id of the individual whose time capability to be looked up")


class TimeCapabilitySearchTool(BaseTool):
    """Tool that queries time capability of an individual and gets back results"""

    name: str = "time_capability_search_tool"
    description: str = (
        "A search tool optimized for comprehensive, accurate, and trusted results of personal time capabilities."
        " Useful when you need to answer questions about time capabilities of a given individual by employee id."
        " This tool supports decision making on working time slots, number of holidays available and vacations"
        " available for an individual who currently works in the given organization."
        " Input should be an employee id."
        " Note: Always consider current date and time in any case of utilizing this tool."
    )
    args_schema: Type[BaseModel] = TimeCapabilitySearchToolInput

    def _run(
            self,
            employee_id: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool"""
        return get_time_capability(employee_id)

    async def _arun(
            self,
            employee_id: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Use the tool asynchronously"""
        return get_time_capability(employee_id)
