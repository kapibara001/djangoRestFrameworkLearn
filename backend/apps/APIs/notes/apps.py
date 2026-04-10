# Этот файл описывает конфигурацию приложения notes.
# Django использует этот класс во время запуска проекта,
# чтобы зарегистрировать приложение и его настройки.
from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = 'apps.APIs.notes'
    verbose_name = 'Приложение заметок'