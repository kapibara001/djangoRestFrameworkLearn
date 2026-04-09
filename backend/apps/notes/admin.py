# Этот файл настраивает отображение модели Note в админке Django.
# Здесь можно выбрать, какие поля показывать, какие фильтры применять
# и какие поля блокировать от редактирования.
from django.contrib import admin
from .models import Note

# Регистрируем модель Note в админке, чтобы она появилась в панели администратора.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Настройка списка записей в админ-панели
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']

    # Группировка полей в форме админки. Это делает интерфейс удобнее.
    fieldsets = [
        ('Основная информация', {
            'fields': ('title', 'content'),
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    ]