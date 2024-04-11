import os

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from configs.query_context import *

READER_MODEL_API_KEY = None
READER_MODEL = None
QUERY_CONTEXT_ANALYZE_PROMPT = None
QUERY_CONTEXT_ANALYZE_CHAIN = None
QUERY_CONTEXT_ANALYZE_OUTPUT_PARSER = None


class QueryContextAnalysis(BaseModel):
    relevance_on_hf: int = Field()
    relevance_on_personal_matters: int = Field()
    relevance_on_satisfaction: int = Field()
    relevance_on_chat_history: int = Field()
    total_rating: int = Field()


def load_reader_model_api_key() -> str:
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values("../secrets.env")
        READER_MODEL_API_KEY = secrets.get("NVIDIA_API_KEY")
        os.environ["NVIDIA_API_KEY"] = READER_MODEL_API_KEY
    return READER_MODEL_API_KEY


def load_reader_model() -> ChatNVIDIA:
    global READER_MODEL

    if not READER_MODEL:
        load_reader_model_api_key()
        READER_MODEL = ChatNVIDIA(
            model=READER_MODEL_NAME,
            temperature=0.3,
            max_tokens=1024
        )
    return READER_MODEL


def load_query_context_analyze_output_parser() -> JsonOutputParser:
    global QUERY_CONTEXT_ANALYZE_OUTPUT_PARSER

    if not QUERY_CONTEXT_ANALYZE_OUTPUT_PARSER:
        QUERY_CONTEXT_ANALYZE_OUTPUT_PARSER = JsonOutputParser(pydantic_object=QueryContextAnalysis)
    return QUERY_CONTEXT_ANALYZE_OUTPUT_PARSER


def load_query_context_analyze_prompt() -> PromptTemplate:
    global QUERY_CONTEXT_ANALYZE_PROMPT

    if not QUERY_CONTEXT_ANALYZE_PROMPT:
        load_query_context_analyze_output_parser()
        QUERY_CONTEXT_ANALYZE_PROMPT = PromptTemplate(
            input_variables=["query", "chat_history"],
            template=QUERY_CONTEXT_ANALYZE_PROMPT_TEMPLATE,
            template_format="jinja2",
            partial_variables={
                "format_instructions": load_query_context_analyze_output_parser().get_format_instructions()
            }
        )
    return QUERY_CONTEXT_ANALYZE_PROMPT


def load_query_context_analyze_chain() -> LLMChain:
    global QUERY_CONTEXT_ANALYZE_CHAIN

    if not QUERY_CONTEXT_ANALYZE_CHAIN:
        QUERY_CONTEXT_ANALYZE_CHAIN = (
                load_query_context_analyze_prompt() |
                load_reader_model() |
                load_query_context_analyze_output_parser()
        )
    return QUERY_CONTEXT_ANALYZE_CHAIN


def generate_query_context_analysis(query: str, chat_history: list) -> dict:
    query_context_analyze_chain = load_query_context_analyze_chain()
    response = query_context_analyze_chain.invoke({
        "query": query,
        "chat_history": chat_history
    })
    return response
