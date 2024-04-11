from typing import Optional

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool

from utils.time import get_current_datetime


class CurrentDateTimeSearchTool(BaseTool):
    """Tool that results current date and time"""

    name: str = "CurrentDateTimeSearchTool"
    description: str = (
        "A search tool optimized for results of current date and time."
        " Useful when you need to answer questions based on current date and time."
        " No inputs are allowed"
    )

    def _run(
            self,
            query: str | None,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool"""
        return get_current_datetime()

    async def _arun(
            self,
            query: str | None,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously"""
        return get_current_datetime()
