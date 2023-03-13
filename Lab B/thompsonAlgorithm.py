from buildAFN import *
import numpy as np

"""
Función que hace uso de las clases NFA, State y Transition para construir un AFN 
usando el algoritmo de Thomposn a partir de una expresión regular en notación posfija
"""

def thompsonBuild(postfixExp):
    stack = []
    stateCount = 0

    # Mejoramos el código de la función oldNFA ahora usando clases para manejar cada transicion
    for c in postfixExp:
        if c.isalnum() or c == 'ε':
            state1 = f'{stateCount}'
            state2 = f'{stateCount+1}'

            # Create a transition for the character c
            transitions = [Transition(start_state=state1, symbol=c, accept_state=state2)]
            # Create a new NFA with the transition
            nfa = NFA(
                        q=[state1, state2],
                        expr=c, 
                        alphabet=[c], 
                        q0=state1, 
                        f=state2, 
                        transitions=transitions
                        )
            # Push the NFA to the stack
            stateCount += 2
            stack.append(nfa)

        else:
            # Concatenacion
            if c == '.':
                # Pop the last two NFAs from the stack
                nfa2 = stack.pop()
                nfa1 = stack.pop()

                # Create a transition for the concatenation
                transitions = [Transition(
                                            start_state=nfa1.f, 
                                            symbol='ε', 
                                            accept_state=nfa2.q0)]
                # Create a new NFA with the transition
                nfa = NFA(
                            q=nfa1.q + nfa2.q, 
                            expr=nfa1.expr + '.' + nfa2.expr, 
                            alphabet = np.array(list(nfa1.alphabet) + list(nfa2.alphabet)),
                            q0=nfa1.q0, 
                            f=nfa2.f, 
                            transitions=nfa1.transitions + nfa2.transitions + transitions
                            )
                # Push the NFA to the stack
                stack.append(nfa)

            # Union
            elif c == '|' or c == 'ε':
                # Pop the last two NFAs from the stack
                nfa2 = stack.pop()
                nfa1 = stack.pop()

                state1 = f'{stateCount}'
                state2 = f'{stateCount+1}'

                # Create a transition for the union
                transitions = [Transition(
                                            start_state=state1, 
                                            symbol='ε', 
                                            accept_state=nfa1.q0),
                                Transition(
                                            start_state=state1, 
                                            symbol='ε', 
                                            accept_state=nfa2.q0),
                                Transition(
                                            start_state=nfa1.f, 
                                            symbol='ε', 
                                            accept_state=state2),
                                Transition(
                                            start_state=nfa2.f, 
                                            symbol='ε', 
                                            accept_state=state2)]
                # Create a new NFA with the transition
                nfa = NFA(
                            q=nfa1.q + nfa2.q + [state1, state2],
                            expr='(' + nfa1.expr + '|' + nfa2.expr + ')',
                            alphabet = np.array(list(nfa1.alphabet) + list(nfa2.alphabet)),
                            q0=state1,
                            f=state2, 
                            transitions=nfa1.transitions + nfa2.transitions + transitions
                            )
                # Push the NFA to the stack
                stack.append(nfa)
                stateCount += 2

            # Cerradura de Kleene
            elif c == '*' or c == '+':
                # Pop the last NFA from the stack
                nfa = stack.pop()

                state1 = f'{stateCount}'
                state2 = f'{stateCount+1}'

                # Create a transition for the Kleene star
                transitions = [Transition(
                                            start_state=state1, 
                                            symbol='ε', 
                                            accept_state=nfa.q0),
                                Transition(
                                            start_state=nfa.f, 
                                            symbol='ε', 
                                            accept_state=state2),
                                Transition(
                                            start_state=state1, 
                                            symbol='ε', 
                                            accept_state=state2),
                                Transition(
                                            start_state=nfa.f, 
                                            symbol='ε', 
                                            accept_state=nfa.q0)]
                # Create a new NFA with the transition
                nfa = NFA(
                            q=nfa.q + [state1, state2],
                            expr='(' + nfa.expr + ')*',
                            alphabet=nfa.alphabet,
                            q0=state1,
                            f=state2, 
                            transitions=nfa.transitions + transitions
                            )
                # Push the NFA to the stack
                stack.append(nfa)
                stateCount += 2

    # Return the NFA
    lastVal = stack.pop()
    print('Estado Inicial: ' + lastVal.q0)
    print('Estado Final: ' + lastVal.f)
    print("---------------Transiciones---------------\n")  
    for q in lastVal.transitions:
        print(q.start_state + ' -> ' + q.symbol + ' -> ' + q.accept_state)
    return (lastVal)
