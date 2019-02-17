from django.db import models
from django.db.models import PROTECT as P


class Sensor(models.Model):

    component = models.ForeignKey('hardware.Component', on_delete=P, null=False)
    uid = models.CharField(max_length=255, null=False)
    parameter = models.CharField(max_length=255, null=False)
    raw_type_summary = models.CharField(max_length=255, null=False)
    raw_data_type = models.CharField(max_length=255, null=False)
    vsr_unit = models.CharField(max_length=255, null=False)
    vsr_data_type = models.CharField(max_length=255, null=False)
    vsr_min_value = models.FloatField(null=False)
    vsr_max_value = models.FloatField(null=False)
    vsr_accuracy = models.FloatField(null=False)
    context = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'hardware_sensors'

    def __str__(self) -> str:
        return f'{self.component} [{self.uid}]'
