from django.db import models


class Resource(models.Model):
    """Модель ресурсов, доступных на складе."""
    title = models.CharField(verbose_name='Наименование', max_length=256)
    amount = models.FloatField(verbose_name='Количество')
    unit = models.CharField(verbose_name='Единица измерения', max_length=64)
    price = models.DecimalField(verbose_name='Цена за единицу', max_digits=6, decimal_places=2)
    date = models.DateField(verbose_name='Дата последнего поступления')

    def __str__(self):
        """Строковое представление объекта."""
        return self.title
