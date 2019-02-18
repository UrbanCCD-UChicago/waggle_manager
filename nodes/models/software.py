from django.conf import settings
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class Software(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    software = models.ForeignKey('software.Software', on_delete=P, null=False)
    effective_as_of = models.DateTimeField(null=False)

    class Meta:
        db_table = 'node_software'

    def __str__(self) -> str:
        return f'{self.node} {self.software}'


class SoftwareChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_software = models.ForeignKey('nodes.Software', on_delete=P, related_name='as_old_set', null=False)
    new_software = models.ForeignKey('nodes.Software', on_delete=P, related_name='as_new_set', null=True)
    removed_without_replacement = models.BooleanField(default=False)
    comment = models.TextField(null=True, default=None, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_software_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentSoftware(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    software = models.ForeignKey('software.Software', on_delete=P, null=False)
    effective_as_of = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'node_current_software'

    @staticmethod
    def create_materialized_view():
        return """
        CREATE MATERIALIZED VIEW node_current_software AS
            SELECT id, node_id, software_id, effective_as_of
            FROM node_software
            WHERE id NOT IN (
                SELECT DISTINCT old_software_id
                FROM node_software_changes
            )
        """

    @staticmethod
    def refresh_materialized_view(*args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_software')

    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'
