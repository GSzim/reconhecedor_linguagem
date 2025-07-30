# automata/views.py

import os
import time
import logging
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from .forms import GrammarForm, WordTestForm
from .models.grammar import RegularGrammar, Production
from .models.automaton import FiniteAutomaton, Transition
from .services.converters.grammar_to_fa import GrammarToFAConverter
from django.conf import settings

logger = logging.getLogger(__name__)

class GrammarView(View):
    template_name = 'automata/grammar.html'
    
    def get(self, request):
        form = GrammarForm()
        test_form = WordTestForm()
        return render(request, self.template_name, {
            'form': form,
            'test_form': test_form
        })
    
    def post(self, request):
        form = GrammarForm(request.POST)
        test_form = WordTestForm()
        context = {
            'form': form,
            'test_form': test_form
        }
        
        if form.is_valid():
            try:
                # Parse form data
                non_terminals = {nt.strip() for nt in form.cleaned_data['non_terminals'].split(',') if nt.strip()}
                terminals = {t.strip() for t in form.cleaned_data['terminals'].split(',') if t.strip()}
                start_symbol = form.cleaned_data['start_symbol'].strip()
                
                # Validação básica
                if not start_symbol:
                    raise ValueError("Start symbol cannot be empty")
                if not non_terminals:
                    raise ValueError("At least one non-terminal is required")
                if start_symbol not in non_terminals:
                    raise ValueError("Start symbol must be in non-terminals")

                productions = []
                for prod_line in form.cleaned_data['productions'].split('\n'):
                    if '->' in prod_line:
                        left, right = prod_line.split('->', 1)
                        productions.append(Production(
                            left=left.strip(),
                            right=right.strip()
                        ))
                
                # Create grammar
                grammar = RegularGrammar(
                    non_terminals=non_terminals,
                    terminals=terminals,
                    productions=productions,
                    start_symbol=start_symbol
                )
                
                if not grammar.is_regular():
                    messages.warning(request, 'The grammar is not regular!')
                
                # Convert to automaton
                automaton = GrammarToFAConverter.convert(grammar)
                
                # Render automaton graph
                image_filename = f"automaton_{int(time.time())}"
                image_path = automaton.render(
                    os.path.join(settings.MEDIA_ROOT, 'automata', image_filename))
                
                # Prepare context
                context.update({
                    'grammar_valid': True,
                    'grammar_type': grammar.type.name.replace('_', ' ').title(),
                    'automaton_type': automaton.type.name,
                    'graph_image': os.path.join(settings.MEDIA_URL, 'automata', f"{image_filename}.png"),
                    'automaton': automaton
                })
                
                # Store automaton in session for word testing
                request.session['automaton_data'] = {
                    'states': list(automaton.states),
                    'alphabet': list(automaton.alphabet),
                    'transitions': [
                        {'from_state': t.from_state, 'symbol': t.symbol, 'to_state': t.to_state}
                        for t in automaton.transitions
                    ],
                    'start_state': automaton.start_state,
                    'final_states': list(automaton.final_states)
                }
            
            except Exception as e:
                messages.error(request, f'Error processing grammar: {str(e)}')
                logger.exception("Error processing grammar")
        
        return render(request, self.template_name, context)

class TestWordView(View):
    def post(self, request):
        test_form = WordTestForm(request.POST)
        
        if test_form.is_valid():
            start_time = time.time()
            word = test_form.cleaned_data['word']
            result = False
            
            try:
                automaton_data = request.session.get('automaton_data')
                if not automaton_data:
                    messages.error(request, 'No automaton defined. Please create a grammar first.')
                    return redirect('grammar_view')
                
                # Recreate automaton from session data
                automaton = FiniteAutomaton(
                    states=set(automaton_data['states']),
                    alphabet=set(automaton_data['alphabet']),
                    transitions=[
                        Transition(t['from_state'], t['symbol'], t['to_state'])
                        for t in automaton_data['transitions']
                    ],
                    start_state=automaton_data['start_state'],
                    final_states=set(automaton_data['final_states'])
                )
                
                result = automaton.accepts(word)
                execution_time = time.time() - start_time
                
                messages.success(
                    request, 
                    f'The word "{word}" was {"accepted" if result else "rejected"}!'
                )
                
                # Add result to context
                request.session['word_test_result'] = {
                    'word_accepted': result,
                    'test_word': word,
                    'execution_time': execution_time
                }
            
            except Exception as e:
                messages.error(request, f'Error testing word: {str(e)}')
                logger.exception("Error testing word")
        
        return redirect('grammar_view')