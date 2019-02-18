from django.db import models


class Node(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    vsn = models.CharField(max_length=255, unique=True, null=True, default=None)
    tags = models.ManyToManyField('nodes.Tag')

    class Meta:
        db_table = 'nodes_nodes'
    
    def __str__(self) -> str:
        if self.vsn:
            return self.vsn
        return self.id
