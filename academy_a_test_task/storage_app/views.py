from django.db.models import F, Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from storage_app.models import Resource
from storage_app.serializers import ResourceListSerializer


@api_view(['GET', ])
def get_total_coast_view(request):
    """Представление функция для получения общей стоимости запасов на складе."""
    total_cost = Resource.objects.all().aggregate(total_cost=Sum(F('amount') * F('price')))
    return Response(total_cost, status=status.HTTP_200_OK)


class ResourceAPIView(APIView):
    """
    Представление-класс для получения списка ресурсов,
    их добавления, изменения и удаления.
    """
    # Определение парсеров данных запроса
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get(self, request):
        """
        Функция обработки GET-запроса.
        Получение списка ресурсов.
        """
        # Получение списка ресурсов
        queryset = Resource.objects.all().order_by('id')
        # Сериализация полученного списка
        serializer = ResourceListSerializer(queryset, many=True)

        return Response({
            'resources': serializer.data,
            'total_count': len(serializer.data)
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Функция обработки POST-запроса.
        Создание экземпляра ресурса.
        """
        # Получение данных запроса
        input_data = request.data

        # Валидация, сериализация входных данных и создание экземпляра
        serializer = ResourceListSerializer(data=input_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        Функция обработки PUT-запроса.
        Изменение экземпляра ресурса.
        """
        return self._update(request)

    def patch(self, request):
        """
        Функция обработки PATCH-запроса.
        Частичное изменение экземпляра ресурса.
        """
        return self._update(request, True)

    def _update(self, request, partial=False):
        """Вспомогательная функция обновления экземпляра ресурса."""
        # Получение id экземпляра ресурса из данных запроса
        object_id = request.data.get('id')
        # Поиск объекта по полученному id
        resource_obj = get_object_or_404(Resource, id=object_id)

        # Валидация, сериализация входных данных и обновление экземпляра
        serializer = ResourceListSerializer(instance=resource_obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Функция обработки DELETE-запроса.
        Удаление экземпляра ресурса.
        """
        # Получение id экземпляра ресурса из данных запроса
        object_id = request.data.get('id')
        # Поиск объекта по полученному id
        resource_obj = get_object_or_404(Resource, id=object_id)
        # Удаление найденного объекта
        resource_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
