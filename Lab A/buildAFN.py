# Con la expresión postfix, construimos el NFA.

import re
from collections import deque

EPSILON = 'ε'
CONCAT = "."
UNION = "+"
KLEENE_STAR = "*"

class Automaton:
    """Representa un autómata finito no determinista"""

    def __init__(self, initial_state=None, final_states=None, transitions=None):
        self.nodes = []
        self.initial_state = initial_state or self.new_node()
        self.final_states = final_states or set()
        self.transitions = transitions or []

    def new_node(self, is_final=False):
        """Crea un nuevo nodo y lo agrega a la lista de nodos del autómata"""
        node = Node(is_final)
        self.nodes.append(node)
        return node

    def __str__(self):
        state_names = {self.initial_state: "s"}
        for i, state in enumerate(sorted(set(self.final_states))):
            state_names[state] = f"f{i}"
        for i, state in enumerate(sorted(set(self.nodes) - {self.initial_state} - self.final_states)):
            state_names[state] = f"q{i}"

        result = [f"Initial state: {state_names[self.initial_state]}"]
        result.append("Final states: " + ", ".join(state_names[state] for state in sorted(self.final_states)))
        for transition in sorted(self.transitions, key=lambda t: (state_names[t.start_node], t.symbol, state_names[t.end_node])):
            result.append(f"{state_names[transition.start_node]} -- {transition.symbol} -> {state_names[transition.end_node]}")
        return "\n".join(result)

    def add_transition(self, source, target, symbol):
        """Agrega una transición al autómata"""
        self.transitions.append(Transition(source, target, symbol))

    def get_epsilon_closure(self, nodes):
        """Calcula el cierre epsilon de un conjunto de nodos"""
        closure = set(nodes)
        stack = list(nodes)
        while stack:
            node = stack.pop()
            for epsilon_transition in node.transitions.get(EPSILON, []):
                if epsilon_transition.target not in closure:
                    closure.add(epsilon_transition.target)
                    stack.append(epsilon_transition.target)
        return closure

    def get_state(self, nodes):
        """Obtiene un nuevo estado a partir de un conjunto de nodos"""
        state = Node()
        for node in nodes:
            state.is_final = state.is_final or node.is_final
            for symbol, transitions in node.transitions.items():
                for transition in transitions:
                    if transition.target in nodes:
                        state.add_transition(symbol, transition.target)
        return state

    # def to_dfa(self):
    #     """Convierte el autómata en un autómata finito determinista (DFA)"""
    #     dfa = DFA()
    #     initial_state = self.get_epsilon_closure([self.initial_state])
    #     dfa.initial_state = self.get_state(initial_state)
    #     unmarked_states = [dfa.initial_state]
    #     while unmarked_states:
    #         state = unmarked_states.pop()
    #         for symbol in self.get_alphabet():
    #             target = self.get_epsilon_closure(state.get_targets(symbol))
    #             if target:
    #                 target_state = self.get_state(target)
    #                 state.add_transition(symbol, target_state)
    #                 if target_state not in dfa.states:
    #                     unmarked_states.append(target_state)
    #     dfa.final_states = set(state for state in dfa.states if any(node.is_final for node in state.nodes))
    #     return dfa

class Node:
    """Representa un nodo en un autómata finito"""

    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}

    def __lt__(self, other):
        return self.is_final < other.is_final

    def add_transition(self, symbol, target):
        """Agrega una transición a otro nodo"""
        transitions = self.transitions.setdefault(symbol, [])
        transitions.append(Transition(self, target, symbol))

    def get_targets(self, symbol):
        """Obtiene los nodos destino para una transición con el símbolo dado"""
        return [transition.target for transition in self.transitions.get(symbol, [])]

    def __hash__(self):
        """Devuelve un valor hash para el nodo"""
        return id(self)

class Transition:
    """Representa una transición de un nodo a otro"""

    def __init__(self, source, target, symbol):
        self.source = source
        self.target = target
        self.symbol = symbol

def postfixToAFN(regex):
    """Construye un AFN a partir de una expresión regular en notación postfix"""
    stack = []
    for symbol in regex:
        if symbol == CONCAT:
            right_operand = stack.pop()
            left_operand = stack.pop()
            left_operand.add_transition(EPSILON, right_operand)
            stack.append(Automaton(initial_state=left_operand.initial_state, final_states=right_operand.final_states))
        elif symbol == UNION:
            right_operand = stack.pop()
            left_operand = stack.pop()
            initial_state = Node()
            initial_state.add_transition(EPSILON, left_operand.initial_state)
            initial_state.add_transition(EPSILON, right_operand.initial_state)
            final_states = left_operand.final_states.union(right_operand.final_states)
            stack.append(Automaton(initial_state=initial_state, final_states=final_states))
        elif symbol == KLEENE_STAR:
            operand = stack.pop()
            initial_state = Node()
            initial_state.add_transition(EPSILON, operand.initial_state)
            for final_state in operand.final_states:
                final_state.add_transition(EPSILON, operand.initial_state)
            final_states = {initial_state}
            stack.append(Automaton(initial_state=initial_state, final_states=final_states))
        else:
            stack.append(Automaton(initial_state=Node(), final_states={Node(is_final=True)}, transitions=[Transition(Node(), Node(is_final=True), symbol)]))
    return stack.pop()

def printAutomaton(automaton):
    """Muestra en pantalla la representación del autómata finito no determinista"""
    print("Estado inicial:", automaton.initial_state)
    print("Estados finales:", automaton.final_states)
    print("Transiciones:")
    for transition in automaton.transitions:
        print(f"{transition.source} --{transition.symbol}--> {transition.target}")

def main():
    """Función principal"""
    regex = input("Ingrese la expresión regular: ")
    automaton = buildAFN(regex)
    print_automaton(automaton)
    # dfa = automaton.to_dfa()
    # print_automaton(dfa)

# if __name__ == "__main__":
#     main()