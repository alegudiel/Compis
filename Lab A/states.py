# # Representar los estados del AFN de Thompson
from collections import deque

class State:
    """Clase para representar un estado del NFA"""
    id = 0
    
    def __init__(self):
        self.transitions = {}
        self.epsilon_transitions = set()
        self.id = State.id
        State.id += 1
    
    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].add(state)
        else:
            self.transitions[symbol] = {state}
    
    def add_epsilon_transition(self, state):
        self.epsilon_transitions.add(state)
    
    def epsilon_closure(self):
        """Calcula el conjunto de estados alcanzables por transiciones epsilon"""
        closure = {self}
        queue = deque([self])
        while queue:
            current_state = queue.popleft()
            for epsilon_state in current_state.epsilon_transitions:
                if epsilon_state not in closure:
                    closure.add(epsilon_state)
                    queue.append(epsilon_state)
        return closure
    
    def __str__(self):
        return f"State {self.id}"
    
    def __lt__(self, other):
        return self.id < other.id

class NFA:
    """Clase para representar un NFA"""
    def __init__(self, start_state, final_states):
        self.start_state = start_state
        self.final_states = final_states
        self.states = self.get_states()
    
    def get_states(self):
        """Obtiene todos los estados del NFA"""
        closure = self.start_state.epsilon_closure()
        states = set()
        queue = deque(closure)
        while queue:
            current_state = queue.popleft()
            states.add(current_state)
            for symbol, next_states in current_state.transitions.items():
                for next_state in next_states:
                    next_closure = next_state.epsilon_closure()
                    for state in next_closure:
                        if state not in closure:
                            closure.add(state)
                            queue.append(state)
        return states

    @staticmethod
    def concatenate(nfa1, nfa2):
        """Realiza la concatenación de dos NFA"""
        for state in nfa1.final_states:
            state.add_epsilon_transition(nfa2.start_state)
        return NFA(nfa1.start_state, nfa2.final_states)
    
    @staticmethod
    def alternate(nfa1, nfa2):
        """Realiza la alternancia de dos NFA"""
        start_state = State()
        start_state.add_epsilon_transition(nfa1.start_state)
        start_state.add_epsilon_transition(nfa2.start_state)
        final_states = nfa1.final_states.union(nfa2.final_states)
        return NFA(start_state, final_states)
    
    @staticmethod
    def kleene(nfa):
        """Realiza la clausura de Kleene de un NFA"""
        start_state = State()
        final_state = State()
        start_state.add_epsilon_transition(nfa.start_state)
        start_state.add_epsilon_transition(final_state)
        for state in nfa.final_states:
            state.add_epsilon_transition(nfa.start_state)
            state.add_epsilon_transition(final_state)
        return NFA(start_state, {final_state})

