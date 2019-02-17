from django.db import models
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class DeprecatesSoftware(models.Model):

    software = models.ForeignKey('software.Software', on_delete=C, related_name='deprecates_set', null=False)
    deprecates = models.ForeignKey('software.Software', on_delete=P, related_name='deprecated_set', null=False)

    class Meta:
        db_table = 'software_deprecates'
        unique_together = [
            ('software', 'deprecates')
        ]

    def __str__(self) -> str:
        return f'{self.software} deprecates {self.deprecates}'
