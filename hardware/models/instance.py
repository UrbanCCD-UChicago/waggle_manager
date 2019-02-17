from django.db import models
from django.db.models import PROTECT as P


class Instance(models.Model):

    component = models.ForeignKey('hardware.Component', on_delete=P, null=False)
    uid = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'hardware_instances'
        unique_together = [
            ('component', 'uid')
        ]
    
    def __str__(self) -> str:
        return f'{self.uid} [{self.component}]'
