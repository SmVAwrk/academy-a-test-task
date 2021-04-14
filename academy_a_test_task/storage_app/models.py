import logging

from django.db import models

logger = logging.getLogger(__name__)


class Resource(models.Model):
    """Модель ресурсов, доступных на складе."""
    title = models.CharField(verbose_name='Наименование', max_length=256)
    amount = models.FloatField(verbose_name='Количество')
    unit = models.CharField(verbose_name='Единица измерения', max_length=64)
    price = models.FloatField(verbose_name='Цена за единицу')
    date = models.DateField(verbose_name='Дата последнего поступления')

    def __str__(self):
        """Определение названия, как строковое представление объекта."""
        return self.title

    def get_cost(self):
        """Дополнительный метод для расчёта общей стоимости."""
        return round(self.amount * self.price, 2)

    def save(self, *args, **kwargs):
        """Расширение метода save() для добавления логирования."""
        if not self.pk:
            logger.info(f'Создание объекта {self.title}')
        else:
            logger.info(f'Изменение объекта {self.title}')
        super().save(*args, **kwargs)
