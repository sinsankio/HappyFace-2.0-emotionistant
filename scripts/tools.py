from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.hf_rag import generate_query_answer


class UserInput(BaseModel):
    query: str = Field(description="should be a query related to a user input")


class RagSearchTool(BaseTool):
    name = "HappyFaceRagSearchTool"
    description = "Use the tool when you need to answer anything in the context of HappyFace service platform"
    args_schema: Type[BaseModel] = UserInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        return generate_query_answer(query)



class ConsultantTool(BaseTool):
    pass

# @tool("HappyFace Rag Search Tool", args_schema=UserInput)
# def rag_search_tool(query: str) -> str:
#     """Use the tool when you need to answer anything in the context of HappyFace service platform"""
#     return generate_query_answer(query)
