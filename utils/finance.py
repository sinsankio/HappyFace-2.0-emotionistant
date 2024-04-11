import json
import os

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from configs.finance import *

FINANCIAL_CAPABILITY_DB = None
READER_MODEL_API_KEY = None
READER_MODEL = None
FINANCIAL_CAPABILITY_SEARCH_PROMPT = None
FINANCIAL_CAPABILITY_SEARCH_CHAIN = None


def load_financial_capability_db(path: str = "../db/financial_capability.json") -> dict:
    global FINANCIAL_CAPABILITY_DB

    if not FINANCIAL_CAPABILITY_DB:
        with open(path, 'r') as db_file:
            FINANCIAL_CAPABILITY_DB = json.loads(db_file.read())
    return FINANCIAL_CAPABILITY_DB


def load_reader_model_api_key() -> str:
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values("../secrets.env")
        READER_MODEL_API_KEY = secrets.get("NVIDIA_API_KEY")
        os.environ["NVIDIA_API_KEY"] = READER_MODEL_API_KEY
    return READER_MODEL_API_KEY


def load_financial_capability_search_prompt() -> PromptTemplate:
    global FINANCIAL_CAPABILITY_SEARCH_PROMPT

    if not FINANCIAL_CAPABILITY_SEARCH_PROMPT:
        FINANCIAL_CAPABILITY_SEARCH_PROMPT = PromptTemplate(
            input_variables=["financial_capabilities", "query"],
            template=FINANCIAL_CAPABILITY_SEARCH_PROMPT_TEMPLATE,
            template_format="jinja2"

        )
    return FINANCIAL_CAPABILITY_SEARCH_PROMPT


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


def load_financial_capability_search_chain() -> LLMChain:
    global FINANCIAL_CAPABILITY_SEARCH_CHAIN

    if not FINANCIAL_CAPABILITY_SEARCH_CHAIN:
        FINANCIAL_CAPABILITY_SEARCH_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_financial_capability_search_prompt()
        )
    return FINANCIAL_CAPABILITY_SEARCH_CHAIN


def generate_financial_capability_search_results(
        query: str
) -> str:
    financial_capability_search_chain = load_financial_capability_search_chain()
    response = financial_capability_search_chain.invoke({
        "query": query,
        "financial_capabilities": load_financial_capability_db()
    })
    return response["text"]
