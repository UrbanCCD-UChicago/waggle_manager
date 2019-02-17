import networkx as nx
from django.db import models, transaction
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class SoftwareRequires(models.Model):

    software = models.ForeignKey('software.Software', on_delete=C, related_name='software_requirements_set', null=False)
    required_software = models.ForeignKey('software.Software', on_delete=P, related_name='required_set', null=False)

    class Meta:
        db_table = 'software_requires_software'
        unique_together = [
            ('software', 'required_software')
        ]
    
    def __str__(self) -> str:
        return f'{self.software} -> {self.required_software}'

    def save(self, *args, **kwargs) -> None:
        with transaction.atomic():
            super().save(*args, **kwargs)

            graph = nx.DiGraph([(d.software_id, d.required_software_id) for d in SoftwareRequires.objects.all()])

            if len(list(nx.simple_cycles(graph))):
                raise 'Software dependency cycle detected -- rolling back'
