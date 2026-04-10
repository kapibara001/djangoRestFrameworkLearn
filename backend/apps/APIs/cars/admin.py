from django.contrib import admin
from .models import Car

# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основная информация', {
            'fields': ('title', 'description', 'year')
        }),
        ('Дополнительная информация', {
            'fields': ('owners', 'created_at')
        }),
    ]
    
    list_display = ['id', 'title', 'year', 'description', 'owners', 'created_at']
    list_editable = ['title', 'description']
    readonly_fields = ['created_at']
    search_fields = ['title', 'year', 'owners']