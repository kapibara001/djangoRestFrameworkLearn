from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator

# Create your models here.
class Car(models.Model):
    title = models.CharField(verbose_name="Название",
                             max_length=64,
                             help_text="Название автомобиля",
                             null=False)
    description = models.TextField(verbose_name="Описание",
                                   validators=[MaxLengthValidator(2000), MinLengthValidator(100)],
                                   null=False,)
    owners = models.IntegerField(verbose_name="Количество владельцев",
                                 validators=[MinValueValidator(0)],
                                 default=0,
                                 null=False,)
    year = models.IntegerField(verbose_name="Год выпуска",
                                null=False,
                                validators=[MinValueValidator(1850), MaxValueValidator(2026)])
    created_at = models.DateTimeField(verbose_name='Дата добавления',
                                      auto_now_add=True,)
    

    def __str__(self):
        return self.title[:25]
    

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-created_at']
