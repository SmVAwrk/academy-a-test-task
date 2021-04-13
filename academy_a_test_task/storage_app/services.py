from rest_framework.exceptions import ValidationError

from storage_app.models import Resource


def id_validation(object_id):
    if object_id is None:
        raise ValidationError({'id': 'Необходимо указать id ресурса.'})
    resource_obj = Resource.objects.filter(id=object_id).first()
    if not resource_obj:
        raise ValidationError({'id': 'Указан невалидный id.'})
    return resource_obj
