from enum import Enum
from typing import Set, Dict, List, Optional
from dataclasses import dataclass
import graphviz

class AutomatonType(Enum):
    DFA = 1
    NFA = 2
    EPSILON_NFA = 3

@dataclass
class Transition:
    from_state: str
    symbol: str
    to_state: str

class FiniteAutomaton:
    def __init__(self, states: Set[str], alphabet: Set[str], 
                 transitions: List[Transition], start_state: str, 
                 final_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.type = self._determine_type()

    def _determine_type(self) -> AutomatonType:
        transition_dict = {}
        has_epsilon = False
        
        for transition in self.transitions:
            if transition.symbol == '':
                has_epsilon = True
            key = (transition.from_state, transition.symbol)
            if key in transition_dict:
                transition_dict[key].append(transition.to_state)
            else:
                transition_dict[key] = [transition.to_state]
        
        for to_states in transition_dict.values():
            if len(to_states) > 1:
                return AutomatonType.EPSILON_NFA if has_epsilon else AutomatonType.NFA
        
        return AutomatonType.DFA

    def accepts(self, word: str) -> bool:
        current_states = self._epsilon_closure({self.start_state})
        
        for symbol in word:
            next_states = set()
            for state in current_states:
                for transition in self.transitions:
                    if transition.from_state == state and transition.symbol == symbol:
                        next_states.add(transition.to_state)
            current_states = self._epsilon_closure(next_states)
            if not current_states:
                return False
        
        return any(state in self.final_states for state in current_states)

    def _epsilon_closure(self, states: Set[str]) -> Set[str]:
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            for transition in self.transitions:
                if transition.from_state == state and transition.symbol == '':
                    if transition.to_state not in closure:
                        closure.add(transition.to_state)
                        stack.append(transition.to_state)
        
        return closure

    def to_dot(self) -> str:
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')
        
        # Add states
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)
        
        # Add start state arrow
        dot.node('', shape='none')
        dot.edge('', self.start_state)
        
        # Group transitions by (from, to) pairs
        transition_map = {}
        for t in self.transitions:
            if t.symbol == '':
                label = 'ε'
            else:
                label = t.symbol
            key = (t.from_state, t.to_state)
            if key in transition_map:
                transition_map[key].append(label)
            else:
                transition_map[key] = [label]
        
        # Add edges with all symbols
        for (from_state, to_state), symbols in transition_map.items():
            dot.edge(from_state, to_state, label=', '.join(sorted(symbols)))
        
        return dot.source

    def render(self, filename: str, format: str = 'png'):
        dot = graphviz.Source(self.to_dot())
        dot.render(filename, format=format, cleanup=True)
        return f'{filename}.{format}'