from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.hf_rag import generate_query_answer
from utils.tools import get_description_text


class HappyFaceSearchResultsInput(BaseModel):
    """Input for the HappyFace Search Results Tool"""

    query: str = Field(description="search query to look up ONLY about HappyFace's services and functionalities")


class HappyFaceSearchResultsTool(BaseTool):
    """Tool that queries the Factual Contents about HappyFace service and gets back results"""

    name: str = "HappyFaceSearchResultsTool"
    description: str = get_description_text(name)
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
