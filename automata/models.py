# automata/models.py

from django.db import models

class GrammarModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    non_terminals = models.TextField()
    terminals = models.TextField()
    start_symbol = models.CharField(max_length=10)
    productions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name or f"Grammar {self.id}"