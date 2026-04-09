# Содержит представления для обработки запросов api
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Note
from .serializers import NoteSerializer, CreateNoteSerializer, NoteUpdateSerializer


class NoteListCreateView(generics.ListCreateAPIView):
    # Представление для всего списка объектов класса Note
    queryset = Note.objects.all()


    def get_serializer_class(self):
        # Возвращает подходящий сериализатор в зависимости от запроса
        if self.request.method == 'POST':
            return CreateNoteSerializer
        return NoteSerializer
    

    def get(self, request, *args, **kwargs):
        # Обработка get-запроса для получения списка заметок 
        return super().get(request, *args, *kwargs)
    

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return NoteUpdateSerializer
        return NoteSerializer
    

    def update(self, request, *args, **kwargs):
        # Обрабатывает обновление заметки с валидацией

        partial = kwargs.pop('partical', False)

        #instance - получаем то, что нам нужно обновить
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Заметка успешно удалена'},
            status=status.HTTP_204_NO_CONTENT,
        )
