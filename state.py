from langchain_core.messages import BaseMessage
from typing import Sequence, TypedDict, Annotated
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    voz_ativa: bool
    gesto_ativo: bool
    camera_ativa: bool