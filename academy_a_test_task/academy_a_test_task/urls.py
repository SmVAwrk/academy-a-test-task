"""
academy_a_test_task URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from academy_a_test_task import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Storage app
    path('', include('storage_app.urls')),
]


# Подключение Debug Toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]