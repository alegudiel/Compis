# Construir un AFN de Thompson a partir de una expresión regular en notación posfija

import re
from collections import deque
from states import State, NFA

def thompsonConstruction(postfixVal):
    stack = deque()
    for token in postfixVal:
        if re.match(r'[\wɛ]', token):
            state = State()
            state.add_transition(token, State())
            stack.append(NFA(state, {state}))
        elif token == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(NFA.alternate(nfa1, nfa2))
        elif token == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(NFA.concatenate(nfa1, nfa2))
        elif token == '*':
            nfa = stack.pop()
            stack.append(NFA.kleene(nfa))
    return stack.pop()


def printNFA(nfa):
    # Obtenemos los estados del NFA
    states = sorted(list(set().union(nfa.start_state.epsilon_closure(), [nfa.start_state]))) + list(nfa.final_states)

    # Obtenemos las transiciones del NFA
    transitions = sorted(list(set([t for s in states for t in nfa.get_transitions(s)]).difference(set([None]))))



    # Imprimimos las columnas de la tabla
    print(f"{'':^6}|{'|'.join([str(t).center(6) for t in transitions])}|")

    # Imprimimos la línea separadora
    print(f"{'':-^7}+{'+'.join(['-'*6 for _ in transitions])}+")

    # Imprimimos las filas de la tabla
    for s in states:
        # Imprimimos el estado actual
        print(f"{str(s):^6}|", end="")
        # Imprimimos las transiciones correspondientes al estado actual
        for t in transitions:
            targets = sorted([tr.target for tr in nfa.get_transitions(s) if tr.symbol == t])
            if targets:
                print(f"{', '.join([str(tg) for tg in targets]).center(6)}|", end="")
            else:
                print(f"{'':^6}|", end="")
        print()

    # Imprimimos la línea separadora
    print(f"{'':-^7}+{'+'.join(['-'*6 for _ in transitions])}+")


# postfixVal = 'ab.*ab.*'
# nfa = thompsonConstruction(postfixVal)
# printNFA(nfa)
