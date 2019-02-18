from django.conf import settings
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class Hardware(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    instance = models.ForeignKey('hardware.Instance', on_delete=P, null=False)
    effective_as_of = models.DateTimeField(null=False)

    class Meta:
        db_table = 'node_hardware'

    def __str__(self) -> str:
        return f'{self.node} {self.instance}'


class HardwareChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_instance = models.ForeignKey('nodes.Hardware', on_delete=P, related_name='as_old_set', null=False)
    new_instance = models.ForeignKey('nodes.Hardware', on_delete=P, related_name='as_new_set', null=True)
    removed_without_replacement = models.BooleanField(default=False)
    comment = models.TextField(null=True, default=None, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_hardware_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentHardware(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    instance = models.ForeignKey('hardware.Instance', on_delete=P, null=False)
    effective_as_of = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'node_current_hardware'

    @staticmethod
    def create_materialized_view():
        return """
        CREATE MATERIALIZED VIEW node_current_hardware AS
            SELECT id, node_id, instance_id, effective_as_of
            FROM node_hardware
            WHERE id NOT IN (
                SELECT DISTINCT old_instance_id
                FROM node_hardware_changes
            )
        """

    @staticmethod
    def refresh_materialized_view(*args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_hardware')

    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'
