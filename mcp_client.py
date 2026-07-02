import os
from datetime import datetime
from typing import Annotated
import zoneinfo  # Biblioteca nativa do Python para fusos horários

from langchain.tools import tool, BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.types import Command
from langgraph.prebuilt import InjectedState

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_JS_PATH = os.path.join(
    BASE_DIR, "node_modules", "@modelcontextprotocol", "server-filesystem", "dist", "index.js"
)

TARGET_DIRECTORY = "C:/Users/ruben.nascimento/Documents/curso"

mcp_client = MultiServerMCPClient(
    {
        "filesystem": {
            "command": "node",
            "args": [
                SERVER_JS_PATH,
                TARGET_DIRECTORY,
            ],
            "transport": "stdio",
        }
    }
)

@tool
def get_current_time(timezone: str = "Africa/Luanda") -> str:
    """Retorna a data e hora atual formatada para um fuso horário específico.

    Args:
        timezone: O fuso horário desejado no formato IANA (ex: 'Africa/Luanda', 'America/Sao_Paulo').
    """
    try:
        tz = zoneinfo.ZoneInfo(timezone)
        now = datetime.now(tz)
        return now.strftime("Dia da semana: %A | Data: %Y-%m-%d | Hora: %H:%M:%S (%Z)")
    except zoneinfo.ZoneInfoNotFoundError:
        return f"Erro: O fuso horário '{timezone}' não é válido."

@tool
def activate_voice(state: Annotated[dict, InjectedState]) -> Command:
    """Ativa a síntese de voz para que as respostas sejam lidas em voz alta."""
    return Command(update={"voice_active": True})

@tool
def deactivate_voice(state: Annotated[dict, InjectedState]) -> Command:
    """Desativa a síntese de voz."""
    return Command(update={"voice_active": False})

LOCAL_TOOLS: list[BaseTool] = [get_current_time, activate_voice, deactivate_voice]

async def get_all_tools() -> list[BaseTool]:
    mcp_tools = await mcp_client.get_tools()
    return LOCAL_TOOLS + mcp_tools
