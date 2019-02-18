from django import forms

from .models import *


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['id', 'vsn']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].label = 'Node ID'
        self.fields['vsn'].label = 'VSN'
