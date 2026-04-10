from rest_framework import serializers
from django.utils.html import escape
from django.core.exceptions import ValidationError
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'title', 'description', 'owners', 'year', 'created_at']
        read_only_fields = ['id', 'year', 'created_at']


    def validate_title(self, value: str):
        if not value.strip():
            raise ValidationError("Название не может быть пустым!")
        return escape(value.strip())
    

    def validate_description(self, value: str):
        if not value.strip():
            raise ValidationError("Описание не может быть пустым!")
        return escape(value.strip())
    

class CreateCarSrializator(CarSerializer):
    pass


class UpdateCarSerializer(CarSerializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)