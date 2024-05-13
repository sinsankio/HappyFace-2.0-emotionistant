import os

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from configs.consultant import *

READER_MODEL_API_KEY = None
READER_MODEL = None
CONSULTANCY_INIT_PROMPT = None
CONSULTANCY_INIT_CHAIN = None
CONSULTANCY_QUERY_PROMPT = None
CONSULTANCY_QUERY_CHAIN = None


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


def load_consultancy_init_prompt() -> PromptTemplate:
    global CONSULTANCY_INIT_PROMPT

    if not CONSULTANCY_INIT_PROMPT:
        CONSULTANCY_INIT_PROMPT = PromptTemplate(
            input_variables=["personal_profile", "emotion_engagement_profile"],
            template=CONSULTANCY_INIT_PROMPT_TEMPLATE
        )
    return CONSULTANCY_INIT_PROMPT


def load_consultancy_query_prompt() -> PromptTemplate:
    global CONSULTANCY_QUERY_PROMPT

    if not CONSULTANCY_QUERY_PROMPT:
        CONSULTANCY_QUERY_PROMPT = PromptTemplate(
            input_variables=["query", "max_guidelines"],
            template=CONSULTANCY_QUERY_PROMPT_TEMPLATE
        )
    return CONSULTANCY_QUERY_PROMPT


def load_consultancy_init_chain() -> LLMChain:
    global CONSULTANCY_INIT_CHAIN

    if not CONSULTANCY_INIT_CHAIN:
        CONSULTANCY_INIT_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_consultancy_init_prompt()
        )
    return CONSULTANCY_INIT_CHAIN


def load_consultancy_query_chain() -> LLMChain:
    global CONSULTANCY_QUERY_CHAIN

    if not CONSULTANCY_QUERY_CHAIN:
        CONSULTANCY_QUERY_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_consultancy_query_prompt()
        )
    return CONSULTANCY_QUERY_CHAIN


def generate_init_consultancy(
        bio_data_profile: str,
        emotion_engagement_profile: str
) -> str:
    consultancy_chain = load_consultancy_init_chain()
    response = consultancy_chain.invoke({
        "bio_data_profile": bio_data_profile,
        "emotion_engagement_profile": emotion_engagement_profile
    })
    return response["text"]


def generate_query_consultancy(
        query: str,
        max_guidelines: int | str = 10
) -> str:
    consultancy_chain = load_consultancy_query_chain()
    response = consultancy_chain.invoke({
        "query": query,
        "max_guidelines": str(max_guidelines).upper(),
    })
    return response["text"]
