import threading
from langgraph.graph.state import RunnableConfig
from langchain_core.messages import HumanMessage
from graph import build_graph
from rich import print

def main() -> None:
    graph = build_graph()
    config = RunnableConfig(configurable={"thread_id": threading.get_ident()})
    user_input = "Olá, sou o Rubem"
    human_message = HumanMessage(content=user_input)
    result = graph.invoke({"messages": [human_message]}, config=config)
    
    print(result)

    
if __name__ == "__main__":
    main()