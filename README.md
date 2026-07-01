# AVM — Assistente Virtual Multimodal

Assistente pessoal inteligente construído com **LangGraph** e **Ollama**, desenhado para aumentar a produtividade através de conversação natural, execução de ferramentas e suporte a múltiplas modalidades de interação (voz, gesto e câmara).

## Funcionalidades

- **Conversação contextual** — mantém histórico entre turnos através do checkpointer do LangGraph
- **Execução de ferramentas** — cálculo, hora atual por fuso horário e mais
- **Síntese de voz** — integração com Kokoro (ativável por comando: *"ativa a voz"*)
- **Reconhecimento de voz** — integração com Faster-Whisper / OpenAI Whisper
- **Gestos** — suporte a MediaPipe para controlo por gesto
- **Câmara** — visão computacional ativável em tempo de execução
- **Multimodal** — análise de imagens e documentos

## Arquitetura

```
main.py          Loop de conversação e ponto de entrada
graph.py         Grafo LangGraph (nós, router, checkpointer)
state.py         AgentState — mensagens + flags de modalidade
tools.py         Ferramentas disponíveis para o LLM
utils.py         Carregamento do modelo (Ollama)
system_prompt.md Identidade e comportamento do assistente
```

O grafo tem a seguinte estrutura:

```
START → call_llm → [router]
                     ├─ tool_node → call_llm   (quando o LLM chama uma ferramenta)
                     ├─ falar_resposta → END   (quando voz está ativa)
                     └─ END                    (caso normal)
```

## Requisitos

- Python 3.12+
- [Ollama](https://ollama.com/) com o modelo `gemma4:e4b` disponível localmente

## Instalação

```bash
# Instalar dependências com uv
uv sync
```

## Execução

```bash
uv run main.py
```

Escreve `sair` para terminar a sessão.

## Comandos de voz/modalidade

| Comando (linguagem natural)  | Efeito                        |
|------------------------------|-------------------------------|
| "ativa a voz"                | Respostas lidas em voz alta   |
| "desativa a voz"             | Volta ao modo texto           |
| "ativa os gestos"            | Liga reconhecimento de gestos |
| "ativa a câmara"             | Liga a câmara                 |

## Dependências principais

| Pacote            | Função                              |
|-------------------|-------------------------------------|
| `langgraph`       | Orquestração do agente              |
| `langchain`       | Abstração LLM e ferramentas         |
| `langchain-ollama`| Integração com Ollama               |
| `kokoro`          | Síntese de voz (TTS)                |
| `faster-whisper`  | Reconhecimento de voz (STT)         |
| `mediapipe`       | Reconhecimento de gestos            |
| `rich`            | Interface de terminal               |
