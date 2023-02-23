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
    """Imprime el NFA"""
    print("NFA:")
    print("Start state:", nfa.start_state)
    # print("Final states:", nfa.final_states)
    print("States:")
    for state in nfa.states:
        print(state)
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                print(f"\t{symbol} -> {next_state}")
        for epsilon_state in state.epsilon_transitions:
            print(f"\tɛ -> {epsilon_state}")


# postfixVal = 'ab.*ab.*'
# nfa = thompsonConstruction(postfixVal)
# printNFA(nfa)
