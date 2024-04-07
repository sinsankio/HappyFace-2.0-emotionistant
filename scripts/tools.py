from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from utils.consultant import generate_consultancy
from utils.hf_rag import generate_query_answer


class HappyFaceInput(BaseModel):
    query: str = Field(description="should be a query related to a user question belongs to the HappyFace context")


class ConsultancyInput(BaseModel):
    query: Optional[str] = Field(default=None,
                                 description="should be a query related to a personal problem someone currently facing")
    personal_profile: str = Field(
        description="a summarized textual description corresponds to an individual's bio-data profile")
    emotion_engagement_profile: str = Field(
        description='''a summarized textual description corresponds to an individual's emotion engagement profile 
        which consisted of explanations and statistics about expressed emotions during their work time''')
    consultant_chat_history: str = Field(
        description="a conversational message history built between a user and a consultant")


class HappyFaceTool(BaseTool):
    name = "HappyFaceRagSearchTool"
    description = '''Use this tool whenever you're responding to requests related to factual details of the
    HappyFace service platform'''
    args_schema: Type[BaseModel] = HappyFaceInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        return generate_query_answer(query)


class ConsultancyTool(BaseTool):
    name = "HappyFaceConsultantTool"
    description = '''Use this tool when addressing queries within the context of offering consultation, guidance, or 
    assistance to an individual actively seeking solutions for encountered personal problems or challenges'''
    args_schema: Type[BaseModel] = ConsultancyInput

    def _run(
            self,
            personal_profile: str,
            emotion_engagement_profile: str,
            consultant_chat_history: str,
            query: str | None = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        if not query:
            return generate_consultancy(
                personal_profile,
                emotion_engagement_profile,
                consultant_chat_history
            )
        return generate_consultancy(
            personal_profile,
            emotion_engagement_profile,
            consultant_chat_history,
            query
        )

# @tool("HappyFace Rag Search Tool", args_schema=UserInput)
# def rag_search_tool(query: str) -> str:
#     """Use the tool when you need to answer anything in the context of HappyFace service platform"""
#     return generate_query_answer(query)
