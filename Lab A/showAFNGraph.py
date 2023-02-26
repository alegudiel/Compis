from graphviz import Digraph

def nfaGraph(nfa):
    dot = Digraph(comment='NFA')
    dot.attr(rankdir='LR', size='10, 34')
    dot.attr('node', shape='circle')
    
    # Etiquetamos los nodos de inicio y final
    dot.node('start', shape='doublecircle', color='green')
    for state in nfa.final_states:
        dot.node(str(state.id), shape='doublecircle', color='red')
    
    # Etiquetamos los demás nodos por su identificador numérico
    for state in nfa.states:
        if state != nfa.start_state and state not in nfa.final_states:
            dot.node(str(state.id))

    # Agregamos las transiciones
    dot.edge('start', str(nfa.start_state.id), label='ε')

    for state in sorted(nfa.states, key=lambda x: x.id):
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                dot.edge(str(state.id), str(next_state.id), label=symbol)
                # dot.edge(str(state.id), str(next_state.id), label='ε')
        for epsilon_state in state.epsilon_transitions:
            # dot.edge(str(state.id), str(epsilon_state.id), label=symbol)
            dot.edge(str(state.id), str(epsilon_state.id), label='ε')
            
            
    dot.format = 'png'
    dot.render('./Graphs/nfa_graph', view=True)


