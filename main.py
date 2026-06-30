from typing import Annotated, TypedDict
from langgraph.graph import START, END, StateGraph
import operator

# Definir o Estado
class State(TypedDict):
    node_path: Annotated[list[str], operator.add]

# Definir Nodes
def node_a(state: State) -> State:
    output_state: State = {"node_path": ["node_a"]}
    print(f"> node_a", f"{state=}", f"{output_state=}")
    return output_state

def node_b(state: State) -> State:
    output_state: State = {"node_path": ["node_b"]}
    print(f"> node_b", f"{state=}", f"{output_state=}")
    return output_state

# Inicializar Grafo
builder = StateGraph(State)

# Adicionar Nó
#builder.add_node(nome_do_no, funcao_que_representa_o_no)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)

# Adicionar Arestas
#builder.add_edge(no_origem, no_destino)
builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", END)

#compilar grafo
graph = builder.compile()

# visualizar grafo
#print(graph.get_graph().draw_mermaid())

# Pegar resultado
result = graph.invoke({"node_path": []})

# Visualizar o resultado de todo grafo
print()
print(f"{result=}")
print()
