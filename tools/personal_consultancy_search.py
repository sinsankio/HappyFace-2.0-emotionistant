from typing import Type, Optional

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.consultant import generate_query_consultancy
from utils.tools import get_description_text


class PersonalConsultancySearchToolInput(BaseModel):
    """Inputs for Personal Consultancy Results Tool"""

    query: str = Field(
        description="search query which consist both of consultancy request and personal profile recommendation of the "
                    "individual who's seeking consultancy, profile recommendation is already provided to you")


class PersonalConsultancySearchTool(BaseTool):
    """Tool that queries consultancy for an individual and gets back results"""

    name: str = "PersonalConsultancySearchTool"
    description: str = get_description_text(name)
    args_schema: Type[BaseModel] = PersonalConsultancySearchToolInput

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool"""
        return generate_query_consultancy(query)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously"""
        return generate_query_consultancy(query)
