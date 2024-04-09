from typing import Type, Optional

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.consultant import generate_query_consultancy


class PersonalConsultancySearchToolInput(BaseModel):
    """Inputs for Personal Consultancy Results Tool"""

    query: str = Field(description="query which addresses the exact personal problem which someone is currently facing")
    recommendation: str = Field(
        description="profile recommendation corresponds to an individual who's needed a consultancy")


class PersonalConsultancySearchTool(BaseTool):
    """Tool that queries consultancy for an individual and gets back results"""

    name: str = "personal_consultancy_search_tool"
    description: str = (
        "A consultancy search tool optimized for comprehensive, accurate, and trusted consultations on personal issues."
        " Useful when you need to answer questions about personal challenges and emotionally impacting human matters of"
        " individuals."
        " Inputs should be a query and a profile recommendation."
    )
    args_schema: Type[BaseModel] = PersonalConsultancySearchToolInput

    def _run(
            self,
            query: str,
            recommendation: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool"""
        return generate_query_consultancy(query, recommendation)

    async def _arun(
            self,
            query: str,
            recommendation: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously"""
        return generate_query_consultancy(query, recommendation)
