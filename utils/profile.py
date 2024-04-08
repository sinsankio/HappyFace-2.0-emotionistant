import json
import os

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from configs.profile import *

READER_MODEL_API_KEY = None
READER_MODEL = None
PROFILE_SUMMARIZER_PROMPT = None
PROFILE_SUMMARIZER_CHAIN = None
PROFILES_INTO_RECOMMENDATION_PROMPT = None
PROFILE_INTO_RECOMMENDATION_CHAIN = None


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


def load_profile_summarizer_prompt() -> PromptTemplate:
    global PROFILE_SUMMARIZER_PROMPT

    if not PROFILE_SUMMARIZER_PROMPT:
        PROFILE_SUMMARIZER_PROMPT = PromptTemplate(
            input_variables=["profile"],
            template=PROFILE_SUMMARIZER_PROMPT_TEMPLATE,
            template_format="jinja2"
        )
    return PROFILE_SUMMARIZER_PROMPT


def load_profiles_into_recommendation_prompt() -> PromptTemplate:
    global PROFILES_INTO_RECOMMENDATION_PROMPT

    if not PROFILES_INTO_RECOMMENDATION_PROMPT:
        PROFILES_INTO_RECOMMENDATION_PROMPT = PromptTemplate(
            input_variables=["bio_data_profile", "emotion_engagement_profile"],
            template=PROFILES_INTO_RECOMMENDATION_PROMPT_TEMPLATE
        )
    return PROFILES_INTO_RECOMMENDATION_PROMPT


def load_profile_summarizer_chain() -> LLMChain:
    global PROFILE_SUMMARIZER_CHAIN

    if not PROFILE_SUMMARIZER_CHAIN:
        PROFILE_SUMMARIZER_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_profile_summarizer_prompt()
        )
    return PROFILE_SUMMARIZER_CHAIN


def load_profiles_into_recommendation_chain() -> LLMChain:
    global PROFILE_INTO_RECOMMENDATION_CHAIN

    if not PROFILE_INTO_RECOMMENDATION_CHAIN:
        PROFILE_INTO_RECOMMENDATION_CHAIN = LLMChain(
            llm=load_reader_model(),
            prompt=load_profiles_into_recommendation_prompt()
        )
    return PROFILE_INTO_RECOMMENDATION_CHAIN


def generate_summarized_profile(profile: dict) -> str:
    summarizer_chain = load_profile_summarizer_chain()
    json_profile = json.dumps(profile, indent=2)
    response = summarizer_chain.invoke({"profile": json_profile})
    return response["text"]


def generate_profiles_into_recommendation(
        bio_data_profile: str,
        emotion_engagement_profile: str
) -> str:
    recommendation_chain = load_profiles_into_recommendation_chain()
    response = recommendation_chain.invoke({
        "bio_data_profile": bio_data_profile,
        "emotion_engagement_profile": emotion_engagement_profile
    })
    return response["text"]
