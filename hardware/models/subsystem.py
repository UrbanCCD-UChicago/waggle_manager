import networkx as nx
from django.db import models, transaction
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class Subsystem(models.Model):

    parent = models.ForeignKey('hardware.Component', on_delete=P, related_name='as_subsystem_parent_set', null=False)
    child = models.ForeignKey('hardware.Component', on_delete=C, related_name='as_subsystem_child_set', null=False)
    child_quantity = models.PositiveIntegerField(null=False)

    class Meta:
        db_table = 'hardware_subsystems'
        unique_together = [
            ('parent', 'child')
        ]

    def __str__(self) -> str:
        return f'{self.child} -> {self.parent}'

    def save(self, *args, **kwargs) -> None:
        with transaction.atomic():
            super().save(*args, **kwargs)

            graph = nx.DiGraph([(s.parent_id, s.child_id) for s in Subsystem.objects.all()])

            if len(list(nx.simple_cycles(graph))):
                raise 'Cycle detected in subsystems -- rolling back'
