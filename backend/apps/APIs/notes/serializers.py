# serializers.py отвечает за перевод модели Note в JSON и обратно.
# DRF-сериализатор берет Django-модель и описывает, какие поля
# будут видны в API, какие поля можно менять и как проверяются данные.
from rest_framework import serializers
from django.utils.html import escape
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    # Основной сериализатор для модели Note.
    # Он создает поля на основе модели и описывает правила чтения/записи.
    class Meta:
        model = Note
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]
        # Эти поля нельзя менять через API: они генерируются автоматически.
        read_only_fields = ['id', 'created_at', 'updated_at']

    # Методы validate_<field> вызываются автоматически
    # при проверке данных для соответствующего поля.
    def validate_title(self, value: str):
        # Проверяем, что заголовок не пустой и не только пробелы.
        if not value.strip():
            raise serializers.ValidationError('Заголовок не может быть пустым')
        # escape защищает от возможного HTML/JS-кода.
        return escape(value.strip())
    
    def validate_content(self, value: str):
        # Проверяем, что содержание заметки не пустое.
        if not value.strip():
            raise serializers.ValidationError('Содержание не может быть пустым')
        return escape(value.strip())
    

class CreateNoteSerializer(NoteSerializer):
    # Сериализатор для создания новой заметки.
    # Наследует поведение NoteSerializer и пока не изменяет его.
    pass


class NoteUpdateSerializer(NoteSerializer):
    # Сериализатор для обновления заметки.
    # Поля title и content здесь не обязательны, чтобы можно было
    # отправить частичное обновление, например только title.
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)