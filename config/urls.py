# config/urls.py

from django.contrib import admin
from django.urls import path
from automata.views import GrammarView, TestWordView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GrammarView.as_view(), name='grammar_view'),
    path('test-word/', TestWordView.as_view(), name='test_word'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)