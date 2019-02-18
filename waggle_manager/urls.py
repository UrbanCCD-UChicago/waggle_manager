from django.contrib import admin
from django.urls import path, include

from nodes import urls as node_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('nodes/', include(node_urls, namespace='nodes')),
]
