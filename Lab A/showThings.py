# queda pendiente de implementar (mejorar ux)

from graphviz import Digraph

def printNFA(nfa):
    print("========NFA========")
    print("Start state:", nfa.start_state)
    print("\t Transitions:")
    # Imprimir las transiciones de cada estado
    for state in nfa.states:
        # Imprimir las transiciones de cada símbolo
        for symbol, next_states in state.transitions.items():
            # Imprimir las transiciones de cada estado siguiente
            for next_state in next_states:
                print(f"\t {state} -- {symbol} --> {next_state}")
                # Imprimir las transiciones epsilon
            for epsilon_state in state.epsilon_transitions:
                print(f"\t {state} -- ε --> {epsilon_state}")
    print("===================")

def nfaGraph(nfa):
    dot = Digraph(comment='NFA')
    dot.attr(rankdir='LR', size='10, 34')
    dot.attr('node', shape='circle')
    
    # Etiquetamos los nodos de inicio y de aceptación
    dot.node(str(nfa.start_state.id), shape='doublecircle')
    for state in nfa.final_states:
        dot.node(str(state.id), shape='doublecircle')
    
    # Etiquetamos los demás nodos por su identificador numérico
    for state in nfa.states:
        if state != nfa.start_state and state not in nfa.final_states:
            dot.node(str(state.id))

    # Agregamos las transiciones
    for state in sorted(nfa.states, key=lambda x: x.id):
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                dot.edge(str(state.id), str(next_state.id), label=symbol)

            for epsilon_state in state.epsilon_transitions:
                dot.edge(str(state.id), str(epsilon_state.id), label='ε')
                if epsilon_state in nfa.final_states:
                    dot.node(str(epsilon_state.id), shape='doublecircle')

    dot.format = 'png'
    dot.render('./Graphs/nfa_graph', view=True)

