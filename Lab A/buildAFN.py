from toPostfix import InfixToPostfix

class State:
    """
    Clase que representa un estado en el autómata finito.
    """
    def __init__(self, transitions=None, is_final=False):
        self.transitions = transitions or {}
        self.is_final = is_final
    
    def add_transition(self, symbol, state):
        """
        Añade una transición al estado.
        """
        if isinstance(symbol, int):
            symbol = (symbol,)
        if symbol in self.transitions:
            self.transitions[symbol].add(state)
        else:
            self.transitions[symbol] = {state}

    def __str__(self):
        transitions_str = ""
        for symbol, states in self.transitions.items():
            states_str = ",".join(str(s) for s in states)
            transitions_str += f"{symbol} -> {states_str}\n"
        return f"State {id(self)}:\n{transitions_str.strip()}\n{'Final' if self.is_final else ''}"

class NFA:
    """
    Clase que representa un autómata finito no determinístico (NFA).
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"Start: {self.start}\nEnd: {self.end}"

class ThompsonConstruction:
    def __init__(self, regex):
        itp = InfixToPostfix(regex)
        self.postfix = str(itp)
        self.nfa = None
        self.states_count = 0

    def _create_nfa(self):
        nfa_stack = []

        for c in self.postfix:
            if c.isalpha():
                state1 = State(self.states_count)
                state2 = State(self.states_count + 1)
                state1.add_transition(c, state2)
                nfa_stack.append((state1, state2))
                self.states_count += 2

            elif c == '|':
                state1, state2 = nfa_stack.pop()
                state3, state4 = nfa_stack.pop()
                new_start_state = State(self.states_count)
                new_accept_state = State(self.states_count + 1)
                new_start_state.add_transition('ε', state3)
                new_start_state.add_transition('ε', state1)
                state2.add_transition('ε', new_accept_state)
                state4.add_transition('ε', new_accept_state)
                nfa_stack.append((new_start_state, new_accept_state))
                self.states_count += 2

            elif c == '*':
                state1, state2 = nfa_stack.pop()
                new_start_state = State(self.states_count)
                new_accept_state = State(self.states_count + 1)
                new_start_state.add_transition('ε', state1)
                new_start_state.add_transition('ε', new_accept_state)
                state2.add_transition('ε', state1)
                state2.add_transition('ε', new_accept_state)
                nfa_stack.append((new_start_state, new_accept_state))
                self.states_count += 2

            elif c == '.':
                state1, state2 = nfa_stack.pop()
                state3, state4 = nfa_stack.pop()
                state3.add_transition('ε', state1)
                nfa_stack.append((state3, state2))
            else:
                raise ValueError(f'Invalid character {c} in regex')

        start_state, accept_state = nfa_stack.pop()
        self.nfa = NFA(start_state, accept_state)

    def __str__(self):
        return f'{self.nfa}'
    
    def __repr__(self):
        return f'{self.nfa}'

def showAFN(nfa):
    print("Transiciones:")
    for state, transitions in nfa.transitions.items():
        for symbol, next_state in transitions.items():
            for next_state in next_state:
                print(f'{state} -> {symbol} -> {next_state}')
    print("Estado inicial:", nfa.start)
    print("Estado final:", nfa.end)

