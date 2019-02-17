from django.db import models
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class NeedsHardware(models.Model):

    software = models.ForeignKey('software.Software', on_delete=C, null=False)
    component = models.ForeignKey('hardware.Component', on_delete=P, null=False)

    class Meta:
        db_table = 'software_needs_hardware'
        unique_together = [
            ('software', 'component')
        ]

    def __str__(self) -> str:
        return f'{self.software} needs {self.component}'


class ProvidesHardware(models.Model):

    software = models.ForeignKey('software.Software', on_delete=C, null=False)
    component = models.ForeignKey('hardware.Component', on_delete=P, null=False)

    class Meta:
        db_table = 'software_provides_hardware'
        unique_together = [
            ('software', 'component')
        ]

    def __str__(self) -> str:
        return f'{self.software} provides {self.component}'


class RecognizesHardware(models.Model):

    software = models.ForeignKey('software.Software', on_delete=C, null=False)
    component = models.ForeignKey('hardware.Component', on_delete=P, null=False)

    class Meta:
        db_table = 'software_recognizes_hardware'
        unique_together = [
            ('software', 'component')
        ]

    def __str__(self) -> str:
        return f'{self.software} recognizes {self.component}'
