import os
from datetime import datetime
import zoneinfo  # Biblioteca nativa do Python para fusos horários

from langchain.tools import tool, BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

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
def multiply(a: float, b: float) -> float:
    """Multiply a * b and returns the result

    Args:
        a: float multiplicand
        b: float multiplier

    Returns:
        the resulting float of the equation a * b
    """
    return a * b

@tool
def get_current_time(timezone: str = "Africa/Luanda") -> str:
    """Retorna a data e hora atual formatada para um fuso horário específico.

    Args:
        timezone: O fuso horário desejado no formato IANA (ex: 'Africa/Luanda', 'America/Sao_Paulo').
    """
    try:
        tz = zoneinfo.ZoneInfo(timezone)
        agora = datetime.now(tz)
        return agora.strftime("Dia da semana: %A | Data: %Y-%m-%d | Hora: %H:%M:%S (%Z)")
    except zoneinfo.ZoneInfoNotFoundError:
        return f"Erro: O fuso horário '{timezone}' não é válido."

LOCAL_TOOLS: list[BaseTool] = [multiply, get_current_time]

async def get_all_tools() -> list[BaseTool]:
    mcp_tools = await mcp_client.get_tools()
    return LOCAL_TOOLS + mcp_tools
