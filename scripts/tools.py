from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.consultant import generate_consultancy
from utils.hf_rag import generate_query_answer


class HappyFaceInput(BaseModel):
    query: str = Field(description="should be a query related to a user question belongs to the HappyFace context")


class HappyFaceTool(BaseTool):
    name = "HappyFaceRagSearchTool"
    description = '''Use this tool whenever you're responding to requests related to factual details of the
    HappyFace service platform'''
    args_schema: Type[BaseModel] = HappyFaceInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        return generate_query_answer(query)

# @tool("HappyFace Rag Search Tool", args_schema=UserInput)
# def rag_search_tool(query: str) -> str:
#     """Use the tool when you need to answer anything in the context of HappyFace service platform"""
#     return generate_query_answer(query)
