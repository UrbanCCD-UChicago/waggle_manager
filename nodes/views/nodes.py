from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from ..forms import NodeForm
from ..models import Node


class NodeListView(ListView):
    model               = Node
    context_object_name = 'nodes'
    
    queryset = Node.objects.all()\
        .prefetch_related('current_state')\
        .prefetch_related('current_ssh_config')\
        .prefetch_related('current_location')


class NodeDetailView(DetailView):
    model               = Node
    slug_field          = 'vsn'
    slug_url_kwarg      = 'vsn'
    context_object_name = 'node'
    
    queryset = Node.objects.all()\
        .prefetch_related('current_description')\
        .prefetch_related('current_hardware')\
        .prefetch_related('current_location')\
        .prefetch_related('current_software')\
        .prefetch_related('current_ssh_config')\
        .prefetch_related('current_ssl_cert')\
        .prefetch_related('current_state')\
        .prefetch_related('current_telephony_id')\
        .prefetch_related('tags')


class NodeCreateView(CreateView):
    model         = Node
    form_class    = NodeForm
    template_name = 'nodes/node_create.html'


class NodeUpdateView(UpdateView):
    model               = Node
    form_class          = NodeForm
    template_name       = 'nodes/node_edit.html'
    slug_field          = 'vsn'
    slug_url_kwarg      = 'vsn'
    context_object_name = 'node'
