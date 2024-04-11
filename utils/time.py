import json
import os
from datetime import datetime

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from configs.time import *

TIME_CAPABILITY_DB = None
READER_MODEL_API_KEY = None
READER_MODEL = None
TIME_CAPABILITY_SEARCH_PROMPT = None
TIME_CAPABILITY_SEARCH_CHAIN = None


def load_time_capability_db(path: str = "../db/time_capability.json") -> dict:
    global TIME_CAPABILITY_DB

    if not TIME_CAPABILITY_DB:
        with open(path, 'r') as db_file:
            TIME_CAPABILITY_DB = json.loads(db_file.read())
    return TIME_CAPABILITY_DB


def get_current_datetime(format: str = "%A, %d %B %Y %I:%M %p") -> str:
    current_datetime = datetime.now()
    return current_datetime.strftime(format)


def load_reader_model_api_key() -> str:
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values("../secrets.env")
        READER_MODEL_API_KEY = secrets.get("NVIDIA_API_KEY")
        os.environ["NVIDIA_API_KEY"] = READER_MODEL_API_KEY
    return READER_MODEL_API_KEY


def load_time_capability_search_prompt() -> PromptTemplate:
    global TIME_CAPABILITY_SEARCH_PROMPT

    if not TIME_CAPABILITY_SEARCH_PROMPT:
        TIME_CAPABILITY_SEARCH_PROMPT = PromptTemplate(
            input_variables=["time_capabilities", "query"],
            template=TIME_CAPABILITY_SEARCH_PROMPT_TEMPLATE,
            template_format="jinja2"

        )
    return TIME_CAPABILITY_SEARCH_PROMPT


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


def load_time_capability_search_chain() -> LLMChain:
    global TIME_CAPABILITY_SEARCH_CHAIN

    if not TIME_CAPABILITY_SEARCH_CHAIN:
        TIME_CAPABILITY_SEARCH_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_time_capability_search_prompt()
        )
    return TIME_CAPABILITY_SEARCH_CHAIN


def generate_time_capability_search_results(
        query: str
) -> str:
    time_capability_search_chain = load_time_capability_search_chain()
    response = time_capability_search_chain.invoke({
        "query": query,
        "time_capabilities": load_time_capability_db()
    })
    return response["text"]
