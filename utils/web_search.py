import os
from typing import Any

from dotenv import dotenv_values
from langchain_community.tools.tavily_search import TavilyAnswer

WEB_SEARCH_SERVICE_API_KEY = None
WEB_SEARCH_ANSWER_TOOL = None


def load_web_search_service_api_key() -> str:
    global WEB_SEARCH_SERVICE_API_KEY

    if not WEB_SEARCH_SERVICE_API_KEY:
        secrets = dotenv_values("../secrets.env")
        WEB_SEARCH_SERVICE_API_KEY = secrets.get("TAVILY_API_KEY")
        os.environ["TAVILY_API_KEY"] = WEB_SEARCH_SERVICE_API_KEY
    return WEB_SEARCH_SERVICE_API_KEY


def load_web_search_answer_tool() -> Any:
    global WEB_SEARCH_ANSWER_TOOL

    if not WEB_SEARCH_ANSWER_TOOL:
        load_web_search_service_api_key()
        WEB_SEARCH_ANSWER_TOOL = TavilyAnswer()
    return WEB_SEARCH_ANSWER_TOOL
