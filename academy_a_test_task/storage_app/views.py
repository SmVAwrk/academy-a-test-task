import logging

from django.db.models import F, Sum
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from storage_app.models import Resource
from storage_app.serializers import ResourceSerializer
from storage_app.services import id_validation

logger = logging.getLogger(__name__)


@api_view(['GET', ])
def index(request, *args, **kwargs):
    return redirect('resources')


@api_view(['GET', ])
def get_total_coast_view(request, *args, **kwargs):
    """Представление функция для получения общей стоимости запасов на складе."""
    total_cost = Resource.objects.all().aggregate(total_cost=Sum(F('amount') * F('price')))

    # Обработка полученного значения
    total_cost['total_cost'] = round(total_cost['total_cost'], 2) if total_cost['total_cost'] else 0

    return Response(total_cost, status=status.HTTP_200_OK)


class ResourceAPIView(APIView):
    """
    Представление-класс для получения списка ресурсов,
    их добавления, изменения и удаления.
    """
    # Определение парсеров данных запроса
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get(self, request, *args, **kwargs):
        """
        Функция обработки GET-запроса.
        Получение списка ресурсов.
        """
        # Получение списка ресурсов
        queryset = Resource.objects.all().order_by('id')
        # Сериализация полученного списка
        serializer = ResourceSerializer(queryset, many=True)

        return Response({
            'resources': serializer.data,
            'total_count': len(serializer.data)
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Функция обработки POST-запроса.
        Создание экземпляра ресурса.
        """
        # Получение данных запроса
        input_data = request.data
        # Валидация, сериализация входных данных и создание экземпляра
        serializer = ResourceSerializer(data=input_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        Функция обработки PUT-запроса.
        Изменение экземпляра ресурса.
        """
        return self._update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Функция обработки PATCH-запроса.
        Частичное изменение экземпляра ресурса.
        """
        return self._update(request, partial=True, *args, **kwargs)

    def _update(self, request, partial=False, *args, **kwargs):
        """Вспомогательная функция обновления экземпляра ресурса."""
        # Получение id экземпляра ресурса из данных запроса
        object_id = request.data.get('id')
        # Поиск объекта по полученному id
        resource_obj = id_validation(object_id)

        # Валидация, сериализация входных данных и обновление экземпляра
        serializer = ResourceSerializer(instance=resource_obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Функция обработки DELETE-запроса.
        Удаление экземпляра ресурса.
        """
        # Получение id экземпляра ресурса из данных запроса
        object_id = request.data.get('id')
        # Поиск объекта по полученному id
        resource_obj = id_validation(object_id)
        logger.info(f'Удаление {resource_obj}')

        # Удаление найденного объекта
        resource_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
