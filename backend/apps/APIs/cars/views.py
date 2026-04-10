
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Car
from .serializers import CarSerializer, CreateCarSrializator, UpdateCarSerializer


# В классе CarListCreateView реализованы методы для получения списка 
# автомобилей и создания нового автомобиля.
class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all()


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCarSrializator
        return CarSerializer
    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
# В классе CarDetailView реализованы методы для получения, обновления и удаления
# конкретного автомобиля по его ID.
class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()

    # Динамический выбор сериализатора в зависимости от типа запроса (GET, PUT, PATCH)
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateCarSerializer
        return CarSerializer


    def update(self, request, *args, **kwargs):
        # Для частичного обновления (PATCH) устанавливаем partical=True, для полного (PUT) - False
        partical = kwargs.pop('partical', False)

        # Получаем текущий экземпляр автомобиля из базы данных
        instance = self.get_object()

        # Создаем сериализатор с текущим экземпляром и данными из запроса, указывая partical для частичного обновления
        serializer = self.get_serializer(instance, data=request.data, partial=partical)

        # Проверяем валидность данных
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        
        # Если данные не валидны, возвращаем ошибки с HTTP 400 Bad Request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Переопределяем метод destroy для удаления автомобиля и возвращения кастомного сообщения
    def destroy(self, request, *args, **kwargs):
        # Получаем экземпляр автомобиля, который нужно удалить
        instance = self.get_object()

        # Удаляем автомобиль из базы данных
        self.perform.destroy(instance)

        # Возвращаем кастомное сообщение с HTTP 204 No Content, так как ресурс удален и нет данных для возвращения
        return Response(
            {'message': 'Автомобиль удален'},
            status=status.HTTP_204_NO_CONTENT,
        )