import json
import os

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from configs.consultant import *

READER_MODEL_API_KEY = None
READER_MODEL = None
SUMMARIZER_PROMPT = None
SUMMARIZER_LLM_CHAIN = None
CONSULTANCY_INIT_PROMPT = None
CONSULTANCY_INIT_LLM_CHAIN = None
CONSULTANCY_QUERY_PROMPT = None
CONSULTANCY_QUERY_LLM_CHAIN = None


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


def load_summarizer_prompt() -> PromptTemplate:
    global SUMMARIZER_PROMPT

    if not SUMMARIZER_PROMPT:
        SUMMARIZER_PROMPT = PromptTemplate(
            input_variables=["profile"],
            template=SUMMARIZER_PROMPT_TEMPLATE,
            template_format="jinja2"
        )
    return SUMMARIZER_PROMPT


def load_consultancy_init_prompt() -> PromptTemplate:
    global CONSULTANCY_INIT_PROMPT

    if not CONSULTANCY_INIT_PROMPT:
        CONSULTANCY_INIT_PROMPT = PromptTemplate(
            input_variables=["personal_profile", "emotion_engagement_profile", "chat_history"],
            template=CONSULTANCY_INIT_PROMPT_TEMPLATE
        )
    return CONSULTANCY_INIT_PROMPT


def load_consultancy_query_prompt() -> PromptTemplate:
    global CONSULTANCY_QUERY_PROMPT

    if not CONSULTANCY_QUERY_PROMPT:
        CONSULTANCY_QUERY_PROMPT = PromptTemplate(
            input_variables=["personal_profile", "emotion_engagement_profile", "chat_history", "query"],
            template=CONSULTANCY_QUERY_PROMPT_TEMPLATE
        )
    return CONSULTANCY_QUERY_PROMPT


def load_summarizer_llm_chain() -> LLMChain:
    global SUMMARIZER_LLM_CHAIN

    if not SUMMARIZER_LLM_CHAIN:
        SUMMARIZER_LLM_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_summarizer_prompt()
        )
    return SUMMARIZER_LLM_CHAIN


def load_consultancy_init_llm_chain() -> LLMChain:
    global CONSULTANCY_INIT_LLM_CHAIN

    if not CONSULTANCY_INIT_LLM_CHAIN:
        CONSULTANCY_INIT_LLM_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_consultancy_init_prompt()
        )
    return CONSULTANCY_INIT_LLM_CHAIN


def load_consultancy_query_llm_chain() -> LLMChain:
    global CONSULTANCY_QUERY_LLM_CHAIN

    if not CONSULTANCY_QUERY_LLM_CHAIN:
        CONSULTANCY_QUERY_LLM_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_consultancy_query_prompt()
        )
    return CONSULTANCY_QUERY_LLM_CHAIN


def generate_summarized_profile(profile: dict) -> str:
    summarizer_chain = load_summarizer_llm_chain()
    json_profile = json.dumps(profile, indent=2)
    response = summarizer_chain.invoke({"profile": json_profile})
    return response["text"]


def generate_init_consultancy(
        personal_profile: str,
        emotion_engagement_profile: str,
        chat_history: list
) -> str:
    consultancy_chain = load_consultancy_init_llm_chain()
    response = consultancy_chain.invoke({
        "personal_profile": personal_profile,
        "emotion_engagement_profile": emotion_engagement_profile,
        "chat_history": chat_history
    })
    return response["text"]


def generate_query_consultancy(
        personal_profile: str,
        emotion_engagement_profile: str,
        chat_history: list,
        query: str
) -> str:
    consultancy_chain = load_consultancy_init_llm_chain()
    response = consultancy_chain.invoke({
        "personal_profile": personal_profile,
        "emotion_engagement_profile": emotion_engagement_profile,
        "chat_history": chat_history,
        "query": query
    })
    return response["text"]
