from langgraph.graph.state import CompiledStateGraph
from typing import Literal
from langgraph.graph import START, END, StateGraph, add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
from pydantic import ValidationError
from pathlib import Path
from rich import print

from state import AgentState
from utils import load_llm
from mcp_client import get_all_tools

TARGET_DIRECTORY = "C:/Users/ruben.nascimento/Documents/curso"

SYSTEM_PROMPT = (
    Path("system_prompt.md")
    .read_text(encoding="utf-8")
    .format(TARGET_DIRECTORY=TARGET_DIRECTORY)
)

def make_call_llm(all_tools: list):
    llm_with_tools = load_llm().bind_tools(all_tools)

    async def call_llm(state: AgentState) -> AgentState:
        system_prompt = SystemMessage(content=SYSTEM_PROMPT)
        result = await llm_with_tools.ainvoke([system_prompt] + state["messages"])
        return {"messages": [result]}

    return call_llm

def make_tool_node(tools_by_name: dict):
    async def tool_node(state: AgentState) -> AgentState:
        llm_response = state["messages"][-1]

        if not isinstance(llm_response, AIMessage) or not getattr(llm_response, "tool_calls", None):
            return state

        call = llm_response.tool_calls[-1]
        name, args, id_ = call["name"], call["args"], call["id"]

        try:
            content = await tools_by_name[name].ainvoke(args)
            status = "success"
        except (KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
            content = f"Please, fix your mistake: {error}"
            status = "error"

        tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)

        return {"messages": [tool_message]}

    return tool_node

def router(state: AgentState) -> Literal["tool_node", "__end__"]:
    llm_response = state["messages"][-1]

    if getattr(llm_response, "tool_calls", None):
        return "tool_node"
    return "__end__"


async def build_graph() -> CompiledStateGraph[AgentState, None, AgentState, AgentState]:
    all_tools = await get_all_tools()
    tools_by_name = {t.name: t for t in all_tools}

    builder = StateGraph(AgentState)

    builder.add_node("call_llm", make_call_llm(all_tools))
    builder.add_node("tool_node", make_tool_node(tools_by_name))

    builder.add_edge(START, "call_llm")
    builder.add_conditional_edges("call_llm", router, ["tool_node", "__end__"])
    builder.add_edge("tool_node", "call_llm")

    return builder.compile(checkpointer=InMemorySaver())
