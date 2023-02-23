from graphviz import Digraph

def nfaGraph(nfa):
    dot = Digraph(comment='NFA')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='doublecircle')
    for state in nfa.final_states:
        state_prefix = 's' # Aquí se define el prefijo personalizado
        dot.node(state_prefix + str(state.id))
    dot.attr('node', shape='circle')
    dot.node('start', shape='point')
    dot.edge('start', 'q' + str(nfa.start_state.id))
    for state in nfa.states:
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                dot.edge('q' + str(state.id), 'q' + str(next_state.id), label=symbol)
        for eps_state in state.epsilon_closure():
            if eps_state in nfa.final_states:
                dot.edge('q' + str(state.id), 'q' + str(eps_state.id), label='ε', style='dashed')
            else:
                dot.edge('q' + str(state.id), 'q' + str(eps_state.id), label='ε', style='dashed')
    dot.format = 'png'
    dot.render('./Lab A/Graphs/nfa_graph', view=True)

