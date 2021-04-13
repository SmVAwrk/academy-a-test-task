from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from storage_app.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    cost = serializers.FloatField(read_only=True, source='get_cost')

    class Meta:
        model = Resource
        fields = ('title', 'id', 'amount', 'unit', 'price', 'cost', 'date')

    def validate_amount(self, value):
        if value < 0:
            raise ValidationError('Количество не может быть меньше 0.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise ValidationError('Цена не может быть меньше 0.')
        return value
