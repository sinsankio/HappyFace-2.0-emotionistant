from dotenv import dotenv_values
from langchain_openai import ChatOpenAI

from configs.agent import *

READER_MODEL_API_KEY = None
READER_MODEL = None


def load_reader_model_api_key():
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values("../secrets.env")
        READER_MODEL_API_KEY = secrets.get("OPENAI_API_KEY")
    return READER_MODEL_API_KEY


def load_reader_model():
    global READER_MODEL

    if not READER_MODEL:
        READER_MODEL = ChatOpenAI(
            temperature=0.7,
            model_name=READER_MODEL_NAME,
            openai_api_key=load_reader_model_api_key()
        )
    return READER_MODEL
