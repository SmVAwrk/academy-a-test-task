from django.contrib import admin

from storage_app.models import Resource

# Регистрация модели в админке
admin.site.register(Resource)
