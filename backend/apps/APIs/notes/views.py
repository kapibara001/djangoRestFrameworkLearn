# ============================================================================
# API представления (Views) для приложения notes
# ============================================================================
# Этот файл содержит классы-представления, которые обрабатывают HTTP-запросы
# к REST API. Они принимают данные, валидируют их через сериализаторы,
# взаимодействуют с моделью базы данных и возвращают JSON-ответы.

from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Note
from .serializers import NoteSerializer, CreateNoteSerializer, NoteUpdateSerializer


# ============================================================================
# NoteListCreateView - Получение списка заметок и создание новой заметки
# ============================================================================
class NoteListCreateView(generics.ListCreateAPIView):
    """
    Класс для обработки операций со списком заметок:
    - GET запрос: возвращает список всех заметок с пагинацией
    - POST запрос: создаёт новую заметку в базе данных
    
    Наследуется от ListCreateAPIView - это готовый класс DRF, который
    предоставляет автоматическую реализацию GET и POST методов.
    """
    
    # Базовый queryset - получаем все заметки из БД для работы с ними
    queryset = Note.objects.all()

    def get_serializer_class(self):
        """
        Динамический выбор сериализатора в зависимости от типа запроса.
        
        Это нужно потому что для разных операций требуется разная валидация
        и структура данных:
        - При POST (создание): используем CreateNoteSerializer с дополнительной валидацией
        - При GET (получение списка): используем базовый NoteSerializer
        
        Returns:
            Класс сериализатора (не экземпляр, а сам класс)
        """
        if self.request.method == 'POST':
            # Для создания новой заметки используем специальный сериализатор
            return CreateNoteSerializer
        
        # Для всех остальных методов (GET, HEAD, OPTIONS) используем обычный
        return NoteSerializer
    
    def get(self, request, *args, **kwargs):
        """
        Обработка GET-запроса для получения списка заметок.
        
        Этот метод вызывает стандартную реализацию из родительского класса
        ListCreateAPIView, которая:
        1. Получает queryset с заметками из БД
        2. Применяет фильтры и пагинацию (если настроены)
        3. Сериализует данные в JSON
        4. Возвращает HTTP 200 с JSON-ответом
        
        Args:
            request: HTTP запрос от клиента
            *args: дополнительные позиционные аргументы
            **kwargs: дополнительные именованные аргументы
        
        Returns:
            Response: JSON-ответ со списком заметок
        """
        return super().get(request, *args, **kwargs)
    

# ============================================================================
# NoteDetailView - Получение, обновление и удаление конкретной заметки
# ============================================================================
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Класс для работы с отдельной заметкой по ID:
    - GET запрос: получить одну заметку по ID
    - PUT запрос: полное обновление заметки (все поля обязательны)
    - PATCH запрос: частичное обновление заметки (можно обновить часть полей)
    - DELETE запрос: удалить заметку
    
    Наследуется от RetrieveUpdateDestroyAPIView - готовый класс DRF
    для работы с отдельными объектами.
    """
    
    # Базовый queryset - все заметки в БД
    queryset = Note.objects.all()

    def get_serializer_class(self):
        """
        Динамический выбор сериализатора в зависимости от типа запроса.
        
        - При PUT/PATCH (обновление): используем NoteUpdateSerializer
        - При GET (получение): используем базовый NoteSerializer
        
        Returns:
            Класс сериализатора для текущего запроса
        """
        if self.request.method in ['PUT', 'PATCH']:
            # Для обновления используем специальный сериализатор
            return NoteUpdateSerializer
        
        # Для получения данных используем обычный сериализатор
        return NoteSerializer

    def update(self, request, *args, **kwargs):
        """
        Обработка PUT и PATCH запросов для обновления заметки.
        
        Эта функция переопределяет поведение по умолчанию, добавляя:
        - Явную валидацию через is_valid()
        - Кастомную обработку ошибок валидации с нужным статус-кодом
        - Возврат обновлённых данных в ответе
        
        Args:
            request: HTTP запрос от клиента с новыми данными в JSON
            *args: дополнительные позиционные аргументы
            **kwargs: дополнительные именованные аргументы
                - 'partial': True для PATCH, False для PUT
        
        Returns:
            Response: JSON с обновленными данными или ошибки валидации
        """
        # Извлекаем флаг partial из kwargs
        # Partial=True означает PATCH (частичное обновление)
        # Partial=False означает PUT (полное обновление)
        partial = kwargs.pop('partial', False)

        # Получаем объект заметки из БД, который нужно обновить
        # get_object() использует ID из URL-адреса (например /notes/1/)
        instance = self.get_object()
        
        # Создаём сериализатор с существующим объектом и новыми данными
        # partial параметр определяет, обязательны ли все поля или можно обновить часть
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # Проверяем валидность полученных данных
        if serializer.is_valid():
            # Данные прошли валидацию - сохраняем обновлённый объект в БД
            self.perform_update(serializer)
            # Возвращаем обновленные данные с кодом 200 OK
            return Response(serializer.data)
        
        # Если валидация не прошла - возвращаем ошибки с кодом 400 Bad Request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
        """
        Обработка DELETE-запроса для удаления заметки.
        
        Этот метод переопределяет поведение по умолчанию для возврата
        более понятного сообщения пользователю при удалении.
        
        Args:
            request: HTTP запрос DELETE от клиента
            *args: дополнительные позиционные аргументы
            **kwargs: дополнительные именованные аргументы
        
        Returns:
            Response: JSON-сообщение об успешном удалении с кодом 204
        """
        # Получаем объект заметки по ID из URL
        instance = self.get_object()
        
        # Удаляем объект из БД
        self.perform_destroy(instance)
        
        # Возвращаем ответ с сообщением и кодом 204 No Content
        # 204 означает, что запрос успешен, но нет содержимого для возврата
        return Response(
            {'message': 'Заметка успешно удалена'},
            status=status.HTTP_204_NO_CONTENT,
        )
