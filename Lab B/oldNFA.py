from toPostfix import infixToPostfix

class NFA:
    def __init__(self, regex):
        self.start_state = None
        self.accept_states = []
        self.transitions = {}

        postfix = infixToPostfix(regex)

        stack = []
        state_count = 0

        for c in postfix:
            if c.isalnum() or c == 'ε':
                state_count += 1
                start_state = f'{state_count}'
                accept_state = f'{state_count+1}'

                self.transitions[(start_state, c)] = [accept_state]
                stack.append((start_state, accept_state))
                state_count += 1

            elif c == '.':
                second_start, second_accept = stack.pop()
                first_start, first_accept = stack.pop()

                self.transitions[(first_accept, 'ε')] = [second_start]
                stack.append((first_start, second_accept))

            elif (c == '|' or c == 'ε'):
                second_start, second_accept = stack.pop()
                first_start, first_accept = stack.pop()

                state_count += 1
                new_start = f'{state_count}'
                state_count += 1
                new_accept = f'{state_count}'

                self.transitions[(new_start, 'ε')] = [first_start, second_start]
                self.transitions[(first_accept, 'ε')] = [new_accept]
                self.transitions[(second_accept, 'ε')] = [new_accept]

                stack.append((new_start, new_accept))

            elif (c == '*' or c == '+'):
                start, accept = stack.pop()

                state_count += 1
                new_start = f'{state_count}'
                state_count += 1
                new_accept = f'{state_count}'

                self.transitions[(new_start, 'ε')] = [start]
                self.transitions[(new_start, 'ε')] = [new_accept]
                self.transitions[(accept, 'ε')] = [start]
                self.transitions[(accept, 'ε')] = [new_accept]

                stack.append((new_start, new_accept))

            elif c == '+':
                start, accept = stack.pop()

                state_count += 1
                new_start = f'{state_count}'
                state_count += 1
                new_accept = f'{state_count}'

                self.transitions[(new_start, 'ε')] = [start]
                self.transitions[(accept, 'ε')] = [new_accept]
                self.transitions[(new_accept, 'ε')] = [new_start]

                stack.append((new_start, new_accept))

        if stack:
            start, accept = stack.pop()
            self.start_state = start
            self.accept_states.append(accept)

    def show(self):
        print(f'Estado inicial: {self.start_state}')
        print(f'Estados de aceptación: {self.accept_states}')
        print('Transiciones:')
        for key, value in self.transitions.items():
            print(f'{key[0]} --{key[1]}--> {value}')

from graphviz import Digraph

def drawNFA(nfa):
    dot = Digraph()
    dot.attr(rankdir='LR')
    dot.engine = 'dot'
    # Estado inicial
    for state in nfa.start_state:
        dot.node(state, state, shape='doublecircle', color='green')

    # Estados de aceptación
    for state in nfa.accept_states:
        dot.node(state, state, shape='doublecircle', color='blue')

    # Transiciones
    for key, value in nfa.transitions.items():
        if key[1] != 'ε':
            for v in value:
                dot.edge(key[0], v, label=key[1])
        else:
            for v in value:
                dot.edge(key[0], v, label='ε')


    dot.render('./Graphs/nfa.gv', view=True)