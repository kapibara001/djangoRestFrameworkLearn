# Определяет сериализаторы для модели Note.
# Сериализаторы - перевод сложных Python-данных в простой читаемый 
# JSON, XML и т.д вид (сериализация) и наоборот (десераеализация).
# Сериализаторы валидируют наши данные (ПРОВЕРЯЮТ).
from rest_framework import serializers
from django.utils.html import escape
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    # Базовый сериализатор для модели Note
    class Meta:
        model = Note
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]
        readonly_fields = ['id', 'created_at', 'updated_at']

    # Валидация 
    # value - то, что передалось для проверки 
    def validate_title(self, value: str):
        # Проверка наличия того, что передали в функцию (в н.случае заголовка) не пустую строку
        if not value.strip():
            raise serializers.ValidationError('Заголовок не может быть пустым')
        return escape(value.strip())
    

    def validate_content(self, value: str):
        # Проверка на то, пустое ли содержание было передано
        if not value.strip():
            raise serializers.ValidationError('Содержание не может быть пустым')
        return escape(value.strip())
    

class CreateNoteSerializer(NoteSerializer):
    pass


# Для обновления заметок
class NoteUpdateSerializer(NoteSerializer):
    # Для обновления заметки title и content деляются необязательными
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)