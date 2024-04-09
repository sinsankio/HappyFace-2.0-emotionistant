from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.hf_rag import generate_query_answer


class HappyFaceSearchResultsInput(BaseModel):
    """Input for the HappyFace Search Results Tool"""

    query: str = Field(description="search query to look up")


class HappyFaceSearchResultsTool(BaseTool):
    """Tool that queries the Factual Contents about HappyFace service and gets back results"""

    name: str = "happyface_search_results_tool"
    description: str = (
        "A search tool optimized for comprehensive, accurate, and trusted results of HappyFace service."
        " Useful when you need to answer questions about features and services about HappyFace platform."
        " Input should be a search query."
    )
    args_schema: Type[BaseModel] = HappyFaceSearchResultsInput

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool"""
        return generate_query_answer(query)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously"""
        return generate_query_answer(query)
