from toPostfix import InfixToPostfix
from collections import deque
from graphviz import Digraph

class State:
    def __init__(self, transitions=None, is_final=False):
        if transitions is None:
            transitions = {}
        self.transitions = transitions
        self.epsilon_closure = set()
        self.is_final = is_final

    def add_transition(self, symbol, next_states):
        if isinstance(next_states, State):
            next_states = [next_states]
        if not isinstance(self.transitions.get(symbol), dict):
            self.transitions[symbol] = {}
        for state in next_states:
            self.transitions[symbol].setdefault(state, set())
            self.transitions[symbol][state].add(state)
            if state.is_final:
                self.is_final = True


    def __str__(self):
        transitions_str = ""
        for symbol, next_states in self.transitions.items():
            next_states_str = ", ".join(str(ns) for ns in next_states)
            transitions_str += f"{symbol} -> {next_states_str}\n"
        epsilon_str = ", ".join(str(s) for s in self.epsilon_closure)
        return f"State {id(self)} ({'Final' if self.is_final else 'Non-final'}):\n{transitions_str.strip()}\n{'ε -> ' + epsilon_str if epsilon_str else ''}"




class NFA:
    def __init__(self, start_state, final_states):
        self.start_state = start_state
        self.final_states = set([final_states])

        self.states = {start_state} | self.final_states
        self.transitions = {start_state: {}}
        self.epsilon = {start_state: set()}

    def add_transition(self, from_state, to_state, symbol=None):
        if from_state not in self.states:
            raise ValueError(f"State {from_state} is not in the NFA.")
        if to_state not in self.states:
            raise ValueError(f"State {to_state} is not in the NFA.")
        if symbol in self.epsilon[from_state]:
            raise ValueError("Epsilon transitions cannot have a symbol.")
        if symbol is None:
            self.epsilon[from_state].add(to_state)
        else:
            if symbol not in self.transitions[from_state]:
                self.transitions[from_state][symbol] = set()
            self.transitions[from_state][symbol].add(to_state)

from graphviz import Digraph

class ThompsonConstruction:
    def __init__(self, regex):
        itp = InfixToPostfix(regex)
        self.postfix = str(itp)
        self.nfa = None
        self.states_count = 0

    def _create_nfa(self):
        nfa_stack = []

        for c in self.postfix:
            if not nfa_stack and c != '*':
                empty_nfa = NFA(State(self.states_count), State(self.states_count + 1))
                self.states_count += 2
                empty_nfa.start_state.add_transition(c, empty_nfa.final_states)
                nfa_stack.append(empty_nfa)
            elif c == '*':
                nfa = nfa_stack.pop()
                start, end = State(self.states_count), State(self.states_count + 1)
                self.states_count += 2
                start.add_transition('ε', [nfa.start_state, end])
                nfa.final_states.add(end)
                nfa.final_states.add(start)
                nfa_stack.append(NFA(start, end))
            elif c == '|':
                nfa2, nfa1 = nfa_stack.pop(), nfa_stack.pop()
                start, end = State(self.states_count), State(self.states_count + 1)
                self.states_count += 2
                start.add_transition('ε', [nfa1.start_state, nfa2.start_state])
                nfa1.final_states.add(end)
                nfa2.final_states.add(end)
                nfa_stack.append(NFA(start, end))
            elif c == '.':
                nfa2, nfa1 = nfa_stack.pop(), nfa_stack.pop()
                nfa1.final_states.add(nfa2.start_state)
                nfa1.final_states.update(nfa2.final_states)
                nfa1.transitions.update(nfa2.transitions)
                nfa_stack.append(nfa1)
            else:
                start, end = State(self.states_count), State(self.states_count + 1)
                self.states_count += 2
                start.add_transition(c, end)
                nfa_stack.append(NFA(start, end))

        if len(nfa_stack) != 1:
            raise ValueError("Invalid regular expression.")

        nfa = nfa_stack.pop()
        for state in nfa.states:
            state.epsilon_closure = self._epsilon_closure(state)

        self.nfa = nfa

    def _epsilon_closure(self, state):
        closure = set()
        visited = set()
        stack = [state]
        while stack:
            s = stack.pop()
            if s in visited:
                continue
            visited.add(s)
            closure.add(s)
            for t in s.epsilon_closure:
                stack.append(t)
        return closure

    def to_graphviz(self, filename=None):
        dot = Digraph(comment='Thompson Construction')
        for state in self.nfa.states:
            label = f"{id(state)}\n{state.is_final}"
            if state == self.nfa.start_state:
                dot.node(str(id(state)), label=label, shape='doublecircle')
            else:
                dot.node(str(id(state)), label=label, shape='circle')
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    dot.edge(str(id(state)), str(id(next_state)), label=symbol)
            for next_state in state.epsilon_closure:
                dot.edge(str(id(state)), str(id(next_state)), label='ε')
        if filename:
            dot.render(filename, view=True)
        else:
            return dot


if __name__ == '__main__':
    regex = "ab|c."
    tc = ThompsonConstruction(regex)
    tc._create_nfa()
    print(tc.to_graphviz())