from rest_framework import serializers

from storage_app.models import Resource


class ResourceListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    cost = serializers.FloatField(read_only=True, source='get_cost')

    class Meta:
        model = Resource
        fields = '__all__'
