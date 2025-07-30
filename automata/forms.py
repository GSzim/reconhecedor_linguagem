from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

class GrammarForm(forms.Form):
    name = forms.CharField(label='Grammar Name', max_length=100)
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea)
    non_terminals = forms.CharField(
        label='Non-Terminals (comma separated)',
        help_text='Example: S,A,B'
    )
    terminals = forms.CharField(
        label='Terminals (comma separated)',
        help_text='Example: a,b'
    )
    start_symbol = forms.CharField(
        label='Start Symbol',
        max_length=1,
        help_text='Example: S'
    )
    productions = forms.CharField(
        label='Productions (one per line)',
        widget=forms.Textarea,
        help_text='Example: S->aA\nA->bB\nB->a'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('start_symbol', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('non_terminals', css_class='form-group col-md-6 mb-0'),
                Column('terminals', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'productions',
            'description',
            Submit('submit', 'Create Grammar')
        )

class WordTestForm(forms.Form):
    word = forms.CharField(label='Test Word', max_length=100)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Test Word'))