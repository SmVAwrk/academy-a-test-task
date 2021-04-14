import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from storage_app.models import Resource

logger = logging.getLogger(__name__)


def id_validation(object_id):
    """
    Функция валидации id ресурса.
    В случае успешной валидации возвращает объект ресурса.
    """
    if object_id is None:
        raise ValidationError({'id': 'Необходимо указать id ресурса.'})
    try:
        resource_obj = Resource.objects.filter(id=object_id).first()
    except Exception:
        raise ValidationError({'id': 'Неверный тип id.'})
    if not resource_obj:
        raise ValidationError({'id': 'Указан невалидный id.'})
    return resource_obj


def custom_exception_handler(exc, context):
    """Кастомный обработчик ошибок при DEBUG = False"""
    response = exception_handler(exc, context)
    if not response:
        logger.error(f'Ошибка: {exc}, контекст: {context}')
        response = Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    return response
