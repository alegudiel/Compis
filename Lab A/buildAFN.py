from collections import deque
from graphviz import Digraph


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
        """Muestra el ID de este estado"""
        return f"State {self.id}"
    
    def __lt__(self, other):
        """Compara este estado con otro estado"""
        return self.id < other.id
    
    # def is_start_state(self):
    #     """Indica si este estado es el estado de inicio"""
    #     return self.id == 0
    
    def is_final_state(self):
        """Indica si este estado es un estado final"""
        return len(self.transitions) == 0
    
    def get_transitions(self, visited_states=set()):
        """Devuelve las transiciones salientes de este estado que no regresan a un estado previo ni sobre sí mismo"""
        transitions = []
        for symbol, states in self.transitions.items():
            for state in states:
                if state not in visited_states and state != self:
                    transitions.append((symbol, state))
        return transitions
    
    def get_epsilon_transitions(self, visited_states=set()):
        """Devuelve las transiciones epsilon salientes de este estado a estados que no han sido visitados antes en el camino actual"""
        epsilon_transitions = []
        for state in self.epsilon_transitions:
            if state not in visited_states:
                epsilon_transitions.append(state)
        return epsilon_transitions
    
    def get_acceptance_states(self):
        """Devuelve los estados de aceptación alcanzables desde este estado"""
        acceptance_states = []
        queue = deque([self])
        while queue:
            current_state = queue.popleft()
            if current_state.is_final_state():
                acceptance_states.append(current_state)
            for symbol, states in current_state.transitions.items():
                for state in states:
                    queue.append(state)
        return acceptance_states

class NFA:
    """Clase para representar un NFA"""
    def __init__(self, start_state, final_states):
        """
        Constructor de la clase NFA.
        Args:
            start_state (State): estado inicial del NFA
            final_states (set<State>): conjunto de estados finales del NFA
        """
        self.start_state = start_state
        self.final_states = final_states
        self.states = self.get_states()
    
    def get_states(self):
        """
        Obtiene todos los estados del NFA.
        Returns:
            set<State>: conjunto de todos los estados del NFA
        """
        # Calcula el cierre epsilon del estado inicial
        closure = self.start_state.epsilon_closure()
        # Inicializa el conjunto de estados
        states = set()
        # Inicializa la cola de estados con el cierre epsilon del estado inicial
        queue = deque(closure)
        while queue:
            current_state = queue.popleft()
            states.add(current_state)
            # Recorre todas las transiciones del estado actual
            for symbol, next_states in current_state.transitions.items():
                # Recorre todos los estados a los que se transita con la transición actual
                for next_state in next_states:
                    # Calcula el cierre epsilon del estado siguiente
                    next_closure = next_state.epsilon_closure()
                    # Agrega los estados del cierre epsilon que no han sido visitados aún
                    for state in next_closure:
                        if state not in closure:
                            closure.add(state)
                            queue.append(state)
        return states

    @staticmethod
    def concatenate(nfa1, nfa2):
        """
        Realiza la concatenación de dos NFA.
        Args:
            nfa1 (NFA): primer NFA
            nfa2 (NFA): segundo NFA
        Returns:
            NFA: nuevo NFA resultante de la concatenación de nfa1 y nfa2
        """
        # Agrega transiciones epsilon desde los estados finales de nfa1 a los estados iniciales de nfa2
        # Creando un nuevo NFA con el estado inicial de nfa1 y los estados finales de nfa2
        for state in nfa1.final_states:
            state.add_epsilon_transition(nfa2.start_state)
        return NFA(nfa1.start_state, nfa2.final_states)
    
    @staticmethod
    def alternate(nfa1, nfa2):
        """
        Realiza la alternancia de dos NFA.
        Args:
            nfa1 (NFA): primer NFA
            nfa2 (NFA): segundo NFA
        Returns:
            NFA: nuevo NFA resultante de la alternancia de nfa1 y nfa2
        """
        # Crea un nuevo estado inicial y agrega transiciones epsilon desde él al estado inicial de nfa1 y nfa2
        start_state = State()
        start_state.add_epsilon_transition(nfa1.start_state)
        start_state.add_epsilon_transition(nfa2.start_state)
        # Une los estados finales de nfa1 y nfa2 en un solo conjunto
        final_states = nfa1.final_states.union(nfa2.final_states)
        # Crea un nuevo NFA con el nuevo estado inicial y los estados finales de nfa1 y nfa2
        return NFA(start_state, final_states)
    
    @staticmethod
    def kleene(nfa):
        """Realiza la clausura de Kleene de un NFA"""

        # Crear el estado inicial y final para el nuevo NFA
        start_state = State()
        final_state = State()

        # Agregar transiciones epsilon desde el estado inicial al estado inicial del NFA original y al estado final del nuevo NFA
        start_state.add_epsilon_transition(nfa.start_state)
        start_state.add_epsilon_transition(final_state)

        # Agregar transiciones epsilon desde cada estado final del NFA original al estado inicial del NFA original y al estado final del nuevo NFA
        for state in nfa.final_states:
            state.add_epsilon_transition(nfa.start_state)
            state.add_epsilon_transition(final_state)

        # Crear y devolver un nuevo objeto NFA con el estado inicial y el estado final recién creados.
        return NFA(start_state, {final_state})

def thompsonConstruction(postfixVal):
    # Crear una pila vacía
    stack = deque()

    # Recorrer cada token en la expresión regular en notación postfix
    for token in postfixVal:
        # Si el token es un caracter alfanumérico o una epsilon, crear un nuevo estado y agregar una transición al siguiente estado
        if token.isalnum() or token == 'ε':
            state = State()
            state.add_transition(token, State())
            stack.append(NFA(state, {state}))
        # Si el token es una barra vertical, pop los dos últimos NFA's de la pila y alternarlos
        elif token == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(NFA.alternate(nfa1, nfa2))
        # Si el token es un punto, pop los dos últimos NFA's de la pila y concatenarlos
        elif token == '.':
            nfa2 = stack.pop()
            # Si la pila está vacía, agregar el segundo NFA a la pila y continuar
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

    dot.format = 'png'
    dot.render('./Graphs/nfa_graph', view=True)


