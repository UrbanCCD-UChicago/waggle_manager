from django.urls import reverse
from django.db import models


class Node(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    vsn = models.CharField(max_length=255, unique=True, null=True, default=None)
    tags = models.ManyToManyField('nodes.Tag', blank=True)

    class Meta:
        db_table = 'nodes_nodes'
    
    def __str__(self) -> str:
        if self.vsn:
            return self.vsn
        return self.id

    def get_absolute_url(self):
        return reverse("nodes:detail", kwargs={"vsn": self.vsn})
