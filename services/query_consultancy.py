import random

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

from configs.agent import AGENT_REACT_PROMPT_TEMPLATE
from configs.agent import MAX_CHAT_HISTORY_MSGS
from tools.financial_capability_search import FinancialCapabilitySearchTool
from tools.happyface_search import HappyFaceSearchResultsTool
from tools.personal_consultancy_search import PersonalConsultancySearchTool
from tools.time_capability_search import TimeCapabilitySearchTool
from utils.agent import load_reader_model
from utils.query_context import generate_query_context_analysis

AGENT_TOOLS: list | None = None
AGENT: Runnable | None = None
AGENT_EXECUTOR: AgentExecutor | None = None
INVALID_QUERY_RESPONSES: list[str] = [
    "Apologies, it appears that the query you entered doesn't match the context I handle. "
    "Please input a valid query or rephrase it for clarity.",

    "I'm sorry, but the query you entered doesn't seem to align with my area of expertise. "
    "Could you please enter a valid query or adjust the format of your current query?",

    "It looks like the query you entered doesn't fit within the scope of what I can assist with. "
    "Please enter a valid query or modify the current one for better understanding.",

    "I apologize, but the query you entered doesn't match the context I specialize in. "
    "Please input a valid query or revise the current one for re-consideration.",

    "Sorry, it seems like the query you entered doesn't align with what I handle. "
    "Could you please enter a valid query or rephrase the current one for better clarity?"
]


def load_agent_tools() -> list:
    global AGENT_TOOLS

    if not AGENT_TOOLS:
        AGENT_TOOLS = [
            HappyFaceSearchResultsTool(),
            PersonalConsultancySearchTool(),
            FinancialCapabilitySearchTool(),
            TimeCapabilitySearchTool()
        ]
    return AGENT_TOOLS


def load_agent() -> Runnable:
    global AGENT

    if not AGENT:
        AGENT = create_react_agent(
            llm=load_reader_model(),
            tools=load_agent_tools(),
            prompt=PromptTemplate.from_template(AGENT_REACT_PROMPT_TEMPLATE)
        )
    return AGENT


def load_agent_executor() -> AgentExecutor:
    global AGENT_EXECUTOR

    if not AGENT_EXECUTOR:
        AGENT_EXECUTOR = AgentExecutor(
            agent=load_agent(),
            tools=load_agent_tools(),
            verbose=True,
            handle_parsing_errors=True
        )
    return AGENT_EXECUTOR


def get_latest_chat_history(chat_history: list) -> list:
    if len(chat_history) > MAX_CHAT_HISTORY_MSGS:
        return chat_history[-1:-(MAX_CHAT_HISTORY_MSGS + 1)]
    return chat_history


def is_valid_query(query: str, chat_history: list, context_match_thresh: int = 2) -> bool:
    context_analysis = generate_query_context_analysis(query, get_latest_chat_history(chat_history))["evaluation"]

    if 'total' in context_analysis:
        return context_analysis['total'] > context_match_thresh
    for val in context_analysis.values():
        if val > context_match_thresh:
            return True
    return False


def generate_agent_user_dialogue(
        query: str,
        agent_output: str,
        user_alias: str = "friend",
        agent_alias: str = "emotionistant"
) -> dict:
    return {
        user_alias: query,
        agent_alias: agent_output
    }


def talk_to_agent(
        query: str,
        organization_name: str,
        employee_id: int | str,
        profile_recommendation: str,
        chat_history: list
) -> dict:
    latest_chat_history = get_latest_chat_history(chat_history)
    if is_valid_query(query, latest_chat_history):
        agent_tools = load_agent_tools()
        result = load_agent_executor().invoke({
            "query": query,
            "organization_name": organization_name,
            "employee_id": employee_id,
            "recommendation": profile_recommendation,
            "chat_history": latest_chat_history,
            "tools": render_text_description(agent_tools),
            "tool_names": ', '.join([tool.name for tool in agent_tools])
        })
        return generate_agent_user_dialogue(query, result["output"])
    return generate_agent_user_dialogue(query, random.choice(INVALID_QUERY_RESPONSES))
