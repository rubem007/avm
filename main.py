import threading
from langgraph.graph.state import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from graph import build_graph
from rich import print
from rich.console import Console

console = Console()

def main() -> None:
    graph = build_graph()
    print(graph.get_graph().draw_mermaid())
    
    # config = RunnableConfig(configurable={"thread_id": threading.get_ident()})
    # initial_state = {
    #     "messages": [],
    #     "voz_ativa": False,
    #     "gesto_ativo": False,
    #     "camera_ativa": False,
    # }

    # graph.invoke(initial_state, config=config)

    # console.print("[bold green]AVM iniciado. Escreve 'sair' para terminar.[/bold green]")

    # while True:
    #     try:
    #         user_input = input("\nTu: ").strip()
    #     except (EOFError, KeyboardInterrupt):
    #         console.print("\n[yellow]A sair...[/yellow]")
    #         break

    #     if user_input.lower() in {"sair", "exit", "quit"}:
    #         console.print("[yellow]A sair...[/yellow]")
    #         break

    #     if not user_input:
    #         continue

    #     result = graph.invoke(
    #         {"messages": [HumanMessage(content=user_input)]},
    #         config=config,
    #     )

    #     last = result["messages"][-1]
    #     if isinstance(last, AIMessage) and last.content:
    #         console.print(f"\n[bold cyan]AVM:[/bold cyan] {last.content}")


if __name__ == "__main__":
    main()
