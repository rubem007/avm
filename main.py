import asyncio
import uuid
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from graph import build_graph
from rich import print
from rich.console import Console

console = Console()

async def conversation() -> None:
    graph = await build_graph()
    config = RunnableConfig(configurable={"thread_id": str(uuid.uuid4())})

    initial_state = {
        "messages": [],
        "voz_ativa": False,
        "gesto_ativo": False,
        "camera_ativa": False,
    }
    await graph.aupdate_state(config, initial_state)

    console.print("[bold green]AVM iniciado. Escreve 'sair' para terminar ou 'historico' para ver a conversa.[/bold green]\n")

    while True:
        try:
            pergunta = await asyncio.to_thread(input, "Tu: ")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold red]A sair...[/bold red]")
            break

        pergunta_limpa = pergunta.strip()
        if not pergunta_limpa:
            continue

        match pergunta_limpa.lower():
            case "sair" | "exit" | "quit":
                console.print("[bold yellow]Até mais![/bold yellow]")
                break
            case "historico":
                estado_atual = await graph.aget_state(config)
                console.print("\n[bold blue]=== Histórico da Conversa ===[/bold blue]")
                for msg in estado_atual.values.get("messages", []):
                    console.print(f"[bold]{type(msg).__name__}:[/bold] {msg.content}")
                console.print("[bold blue]=============================[/bold blue]\n")
                continue

        console.print("[bold cyan]AVM:[/bold cyan] ", end="")

        try:
            async for event in graph.astream_events(
                {"messages": [HumanMessage(content=pergunta_limpa)]},
                config=config,
                version="v2",
            ):
                if event["event"] == "on_chat_model_stream":
                    token = event["data"]["chunk"].content
                    if token:
                        print(token, end="", flush=True)
        except KeyboardInterrupt:
            console.print("\n[bold red]A sair...[/bold red]")
            break
        except Exception as exc:
            console.print(f"\n[bold red][Erro no modelo: {exc}][/bold red]")
            continue
        finally:
            print()


def main() -> None:
    try:
        asyncio.run(conversation())
    except KeyboardInterrupt:
        console.print("\n[bold red]A sair...[/bold red]")


if __name__ == "__main__":
    main()
