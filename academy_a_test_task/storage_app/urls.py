from django.urls import path

from storage_app.views import ResourceAPIView, get_total_coast_view, index

urlpatterns = [
    path('', index),
    path('resources/', ResourceAPIView.as_view(), name='resources'),
    path('total_cost/', get_total_coast_view, name='total_cost'),
]
