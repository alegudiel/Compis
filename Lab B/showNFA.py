"""
Archivo para graficar NFA's
"""

from graphviz import Digraph

def drawNFA(nfa):
    # Create a new directed graph
    dot = Digraph(comment='NFA')

    # Add the initial state
    dot.attr(rankdir='LR', size='10, 34')
    dot.attr('node', shape='doublecircle')
    dot.node(nfa.q0)

    # Add the final states
    dot.attr('node', shape='doublecircle')
    dot.node(nfa.f)

    # Add the transitions
    dot.attr('node', shape='circle')
    for q in nfa.transitions:
        dot.edge(q.start_state, q.accept_state, label=q.symbol)

    # Render the graph
    dot.format = 'png'
    dot.render('./Graphs/nfaGraph', view=True)
