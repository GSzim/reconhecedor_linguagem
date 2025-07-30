from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Dict

class GrammarType(Enum):
    RIGHT_LINEAR = 1
    LEFT_LINEAR = 2
    UNRESTRICTED = 3

@dataclass
class Production:
    left: str
    right: str

class RegularGrammar:
    def __init__(self, non_terminals: Set[str], terminals: Set[str], 
                 productions: List[Production], start_symbol: str):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.type = self._determine_type()

    def _determine_type(self) -> GrammarType:
        is_right = True
        is_left = True
        
        for prod in self.productions:
            # Verifica se a produção é válida para gramática regular
            if len(prod.left) != 1 or prod.left not in self.non_terminals:
                is_right = False
                is_left = False
                break
            
            # Verifica se é right-linear
            right_ok = (len(prod.right) == 1 and prod.right in self.terminals) or \
                      (len(prod.right) == 2 and prod.right[0] in self.terminals and 
                       prod.right[1] in self.non_terminals)
            
            if not right_ok:
                is_right = False
            
            # Verifica se é left-linear
            left_ok = (len(prod.right) == 1 and prod.right in self.terminals) or \
                     (len(prod.right) == 2 and prod.right[-1] in self.terminals and 
                      prod.right[0] in self.non_terminals)
            
            if not left_ok:
                is_left = False
            
            if not is_right and not is_left:
                break
        
        if is_right:
            return GrammarType.RIGHT_LINEAR
        elif is_left:
            return GrammarType.LEFT_LINEAR
        else:
            return GrammarType.UNRESTRICTED

    def is_regular(self) -> bool:
        return self.type != GrammarType.UNRESTRICTED

    def to_finite_automaton(self):
        from ..services.converters.grammar_to_fa import GrammarToFAConverter
        return GrammarToFAConverter.convert(self)