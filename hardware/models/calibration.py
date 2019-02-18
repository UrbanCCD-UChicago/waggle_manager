from django.conf import settings
from django.db import connection, models
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class Calibration(models.Model):

    instance = models.ForeignKey('hardware.Instance', on_delete=C, null=False)
    value = models.CharField(max_length=255, null=False)
    effective_as_of = models.DateTimeField(null=False)

    class Meta:
        db_table = 'hardware_calibrations'

    def __str__(self) -> str:
        return f'{self.instance} [{self.timestamp}]'


class CalibrationChange(models.Model):

    instance = models.ForeignKey('hardware.Instance', on_delete=C, null=False)
    old_calibration = models.ForeignKey('hardware.Calibration', on_delete=C, related_name='as_old_set', null=False)
    new_calibration = models.ForeignKey('hardware.Calibration', on_delete=C, related_name='as_new_set', null=False)
    comment = models.TextField(null=True, default=None, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'hardware_calibration_changes'

    def __str__(self) -> str:
        return f'{self.instance} [{self.created_on}]'


class CurrentCalibration(models.Model):

    instance = models.OneToOneField('hardware.Instance', on_delete=C, related_name='current_calibration', null=False)
    value = models.CharField(max_length=255, null=False)
    effective_as_of = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'hardware_current_calibrations'

    @staticmethod
    def create_materialized_view():
        return """
        CREATE MATERIALIZED VIEW hardware_current_calibrations AS
            SELECT id, instance_id, value, effective_as_of
            FROM hardware_calibrations
            WHERE id NOT IN (
                SELECT DISTINCT old_calibration_id
                FROM hardware_calibration_changes
            )
        """

    @staticmethod
    def refresh_materialized_view(*args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('REFRESH MATERIALIZED VIEW hardware_current_calibrations')

    def __str__(self) -> str:
        return f'{self.instance} [{self.timestamp}]'
