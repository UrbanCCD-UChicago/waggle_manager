from django.db import models


class Component(models.Model):

    name = models.CharField(max_length=255, null=False)
    manufacturer = models.CharField(max_length=255, null=False)
    version = models.CharField(max_length=255, null=False)
    data_sheet = models.CharField(max_length=255, null=True, default=None, blank=True)
    part_number = models.CharField(max_length=255, null=True, default=None, blank=True)
    additional_info = models.CharField(max_length=255, null=True, default=None, blank=True)

    class Meta:
        db_table = 'hardware_components'
        unique_together = [
            ('name', 'manufacturer', 'version')
        ]

    def __str__(self) -> str:
        return f'{self.name} {self.version}'
