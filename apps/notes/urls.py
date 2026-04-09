# определяет url-маршруты для приложения notes
# Связывается с главным config.urls
from django.urls import path
from .views import NoteListCreateView, NoteDetailView

add_name = 'notes'

urlpatterns = [
    path('notes', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:id>', NoteDetailView.as_view(), name='note-detail'),
]