from django.urls import path

from storage_app.views import ResourceAPIView, get_total_coast_view

urlpatterns = [
    path('resources/', ResourceAPIView.as_view()),
    path('total_cost/', get_total_coast_view),
]