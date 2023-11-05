from typing import List, Tuple

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_xml
from langchain.chat_models import ChatAnthropic
from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema import AIMessage, HumanMessage
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools.render import render_text_description

from .prompts import conversational_prompt, parse_output


def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

def get_xml_agent(model, tools, system_message):

    prompt = conversational_prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
        system_message=system_message
    )
    llm_with_stop = model.bind(stop=["</tool_input>"])

    agent = (
        prompt
        | llm_with_stop
        | parse_output
    )
    return agent

