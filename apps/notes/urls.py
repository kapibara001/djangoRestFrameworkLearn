# Этот файл описывает адреса (URL) для API приложения notes.
# Главный файл config.urls подключает этот модуль, и тогда
# все запросы /api/v1/notes/... будут обрабатываться здесь.
from django.urls import path
from .views import NoteListCreateView, NoteDetailView

app_name = 'notes'

urlpatterns = [
    # /api/v1/notes  — список заметок и создание новой заметки.
    path('notes', NoteListCreateView.as_view(), name='note-list-create'),
    # /api/v1/notes/<pk> — просмотр, обновление или удаление конкретной заметки.
    path('notes/<int:pk>', NoteDetailView.as_view(), name='note-detail'),
]