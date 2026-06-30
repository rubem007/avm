from langchain.tools import tool, BaseTool
from datetime import datetime
import zoneinfo  # Biblioteca nativa do Python para fusos horários

@tool
def sum(a: float, b: float) -> float:
    """Sum a + b and returns the result
    
    Args:
        a: float 
        b: float 
        
    Returns:
        the resulting float of the equation a + b
    """
    return a + b

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
        return agora.strftime("Data: %Y-%m-%d | Hora: %H:%M:%S (%Z)")
    except zoneinfo.ZoneInfoNotFoundError:
        return f"Erro: O fuso horário '{timezone}' não é válido."
    
TOOLS: list[BaseTool] = [multiply, get_current_time]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}