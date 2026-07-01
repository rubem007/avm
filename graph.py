from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command
from typing import Literal
from langgraph.graph import START, END, StateGraph, add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
from pydantic import ValidationError
from pathlib import Path
from rich import print

from state import AgentState
from utils import load_llm
from tools import TOOLS, TOOLS_BY_NAME

TARGET_DIRECTORY = "C:/Users/ruben.nascimento/Documents/curso"

SYSTEM_PROMPT = (
    Path("system_prompt.md")
    .read_text(encoding="utf-8")
    .format(TARGET_DIRECTORY=TARGET_DIRECTORY)
)

def call_llm(state: AgentState) -> AgentState:
    llm_with_tools = load_llm().bind_tools(TOOLS)
    system_prompt = SystemMessage(content=SYSTEM_PROMPT)
    result = llm_with_tools.invoke([system_prompt] + state["messages"])

    return {"messages": [result]}

def tool_node(state: AgentState) -> AgentState:
    llm_response = state["messages"][-1]
    
    if not isinstance(llm_response, AIMessage) or not getattr(llm_response, "tool_calls", None):
        return state
    
    call = llm_response.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]
    
    state_updates: dict = {}
    try:
        result = TOOLS_BY_NAME[name].invoke(args)
        if isinstance(result, Command):
            state_updates = result.update or {}
            content = f"OK: {list(state_updates.keys())}"
        else:
            content = str(result)
        status = "success"
    except (KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
        content = f"Please, fix your mistake: {error}"
        status = "error"

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)

    return {"messages": [tool_message], **state_updates}
        
def falar_resposta(state: AgentState) -> AgentState:
    if not state.get("voz_ativa"):
        return state

    last = state["messages"][-1]
    texto = last.content if isinstance(last, AIMessage) else ""
    if texto:
        print(f"[bold magenta][VOZ][/bold magenta] {texto}")
        # Aqui entra a chamada ao Kokoro quando for integrado

    return state

def router(state: AgentState) -> Literal["tool_node", "falar_resposta", "__end__"]:
    llm_response = state["messages"][-1]

    if getattr(llm_response, "tool_calls", None):
        return "tool_node"
    if state.get("voz_ativa"):
        return "falar_resposta"
    return "__end__"


def build_graph() -> CompiledStateGraph[AgentState, None, AgentState, AgentState]:
    builder = StateGraph(AgentState)

    builder.add_node("call_llm", call_llm)
    builder.add_node("tool_node", tool_node)
    builder.add_node("falar_resposta", falar_resposta)

    builder.add_edge(START, "call_llm")
    builder.add_conditional_edges("call_llm", router, ["tool_node", "falar_resposta", "__end__"])
    builder.add_edge("tool_node", "call_llm")
    builder.add_edge("falar_resposta", END)

    return builder.compile(checkpointer=InMemorySaver())
