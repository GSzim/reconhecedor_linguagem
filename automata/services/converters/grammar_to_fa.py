from ...models.grammar import RegularGrammar, Production
from ...models.automaton import FiniteAutomaton, Transition

class GrammarToFAConverter:
    @staticmethod
    def convert(grammar: RegularGrammar) -> FiniteAutomaton:
        if not grammar.is_regular():
            raise ValueError("Grammar is not regular")
        
        # Create states
        states = set(grammar.non_terminals)
        states.add('F')  # Final state
        
        # Create alphabet
        alphabet = set(grammar.terminals)
        
        # Create transitions
        transitions = []
        
        for prod in grammar.productions:
            if len(prod.right) == 1:  # A -> a
                transitions.append(Transition(
                    from_state=prod.left,
                    symbol=prod.right,
                    to_state='F'
                ))
            else:  # A -> aB
                transitions.append(Transition(
                    from_state=prod.left,
                    symbol=prod.right[0],
                    to_state=prod.right[1]
                ))
        
        # Set final states
        final_states = {'F'}
        
        # Check if empty string is in language
        empty_prod = next((p for p in grammar.productions 
                          if p.left == grammar.start_symbol and p.right == ''), None)
        if empty_prod:
            final_states.add(grammar.start_symbol)
        
        return FiniteAutomaton(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            start_state=grammar.start_symbol,
            final_states=final_states
        )