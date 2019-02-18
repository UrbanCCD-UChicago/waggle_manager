from django.urls import path

from .views.nodes import NodeListView, NodeDetailView, NodeCreateView, NodeUpdateView


app_name = 'nodes'

urlpatterns = [
    path('', NodeListView.as_view(), name='list'),
    path('new', NodeCreateView.as_view(), name='create'),
    path('<str:vsn>/edit', NodeUpdateView.as_view(), name='edit'),
    path('<str:vsn>', NodeDetailView.as_view(), name='detail'),
]
