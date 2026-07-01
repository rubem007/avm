from langchain.tools import tool, BaseTool
from langgraph.types import Command
from langgraph.prebuilt import InjectedState
from typing import Annotated
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
    
@tool
def ativar_voz(state: Annotated[dict, InjectedState]) -> Command:
    """Ativa a síntese de voz para que as respostas sejam lidas em voz alta."""
    return Command(update={"voz_ativa": True})

@tool
def desativar_voz(state: Annotated[dict, InjectedState]) -> Command:
    """Desativa a síntese de voz."""
    return Command(update={"voz_ativa": False})

@tool
def ativar_gesto(state: Annotated[dict, InjectedState]) -> Command:
    """Ativa o reconhecimento de gestos."""
    return Command(update={"gesto_ativo": True})

@tool
def desativar_gesto(state: Annotated[dict, InjectedState]) -> Command:
    """Desativa o reconhecimento de gestos."""
    return Command(update={"gesto_ativo": False})

@tool
def ativar_camera(state: Annotated[dict, InjectedState]) -> Command:
    """Ativa a câmara."""
    return Command(update={"camera_ativa": True})

@tool
def desativar_camera(state: Annotated[dict, InjectedState]) -> Command:
    """Desativa a câmara."""
    return Command(update={"camera_ativa": False})

TOOLS: list[BaseTool] = [
    multiply, get_current_time,
    ativar_voz, desativar_voz,
    ativar_gesto, desativar_gesto,
    ativar_camera, desativar_camera,
]
TOOLS_BY_NAME: dict[str, BaseTool] = {t.name: t for t in TOOLS}