# Construir un AFN de Thompson a partir de una expresión regular en notación posfija

import re
from collections import deque
from states import State, NFA

def thompsonConstruction(postfixVal):
    # Crear una pila vacía
    stack = deque()

    # Recorrer cada token en la expresión regular en notación postfix
    for token in postfixVal:
        # Si el token es un caracter alfanumérico o una epsilon, crear un nuevo estado y agregar una transición al siguiente estado
        if re.match(r'[\wɛ]', token):
            state = State()
            state.add_transition(token, State())
            stack.append(NFA(state, {state}))
        # Si el token es una barra vertical, pop los dos últimos NFA's de la pila y alternarlos
        elif token == '|':
            nfa2 = stack.pop()
            # fix error: indexerror: pop from an empty deque
            if len(stack) == 0:
                stack.append(nfa2)
                continue
            nfa1 = stack.pop()
            stack.append(NFA.alternate(nfa1, nfa2))
        # Si el token es un punto, pop los dos últimos NFA's de la pila y concatenarlos
        elif token == '.':
            nfa2 = stack.pop()
            # fix error: indexerror: pop from an empty deque
            if len(stack) == 0:
                stack.append(nfa2)
                continue
            nfa1 = stack.pop()
            stack.append(NFA.concatenate(nfa1, nfa2))
        # Si el token es un asterisco, pop el último NFA de la pila y aplicar la clausura de Kleene
        elif token == '*':
            nfa = stack.pop()
            stack.append(NFA.kleene(nfa))

    # Al final, la única cosa en la pila debería ser el NFA final
    return stack.pop()

def printNFA(nfa):
    """Imprime el NFA"""
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
