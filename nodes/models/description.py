from django.conf import settings
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class Description(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    effective_as_of = models.DateTimeField(null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'node_descriptions'
    
    def __str__(self) -> str:
        return f'{self.node} {self.description} [{self.effective_as_of}]'


class DescriptionChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_description = models.ForeignKey('nodes.Description', on_delete=C, related_name='as_old_set', null=False)
    new_description = models.ForeignKey('nodes.Description', on_delete=C, related_name='as_new_set', null=False)
    comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_description_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentDescription(models.Model):

    node = models.OneToOneField('nodes.Node', on_delete=C, related_name='current_description')
    effective_as_of = models.DateTimeField(null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'node_current_descriptions'

    @staticmethod
    def create_materialized_view():
        return """
        CREATE MATERIALIZED VIEW node_current_descriptions AS
            SELECT id, node_id, description, effective_as_of
            FROM node_descriptions
            WHERE id NOT IN (
                SELECT DISTINCT old_description_id
                FROM node_description_changes
            )
        """

    @staticmethod
    def refresh_materialized_view(*args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_descriptions')

    def __str__(self) -> str:
        return f'{self.node} [{self.timestamp}]'
