class State:
    """
    Clase que representa un estado en el autómata finito.
    """
    def __init__(self, transitions=None, is_final=False):
        self.transitions = transitions or {}
        self.is_final = is_final


class NFA:
    """
    Clase que representa un autómata finito no determinístico (NFA).
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end


class ThompsonConstruction:
    def __init__(self, regex):
        itp = InfixToPostfix(regex)
        self.postfix = str(itp)
        # self.regex = regex
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

    def create_nfa(self):
        self._create_nfa()
        return self.nfa

    def __str__(self):
        return f'{self.nfa}'
    
    def __repr__(self):
        return f'{self.nfa}'
    
    def __len__(self):
        return len(self.nfa)
    
    def __getitem__(self, index):
        return self.nfa[index]
    
    def __setitem__(self, index, value):
        self.nfa[index] = value

def showAFN(nfa):
    print("Transiciones:")
    for state, transitions in nfa.transitions.items():
        for symbol, next_state in transitions.items():
            for next_state in next_state:
                print(f'{state} -> {symbol} -> {next_state}')
    print("Estado inicial:", nfa.start)
    print("Estado final:", nfa.end)


from toPostfix import InfixToPostfix

def main(regex):
    # chequear que este balanceada
    # y convertirlo a su forma postfix
    """
    Construye un AFN a partir de una expresión regular.
    """
    # Crear objeto para expresión regular
    # regex = input("Ingrese la expresión regular: ")
    itp = InfixToPostfix(regex)

    # Chequear que la expresión regular este balanceada
    print("¿Expresión balanceada?", itp.isBalanced())

    # Formatear la expresión regular
    print("Expresion formateada:", itp.formatRegex())

    # Convertir a postfix
    print("Expresion en postfix:", itp)

    # Crear el AFN
    showAFN(ThompsonConstruction(itp).create_nfa())

if __name__ == '__main__':
    regex = input("Ingrese la expresión regular: ")
    main(regex)