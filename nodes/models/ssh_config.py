from django.conf import settings
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class SSHConfig(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    effective_as_of = models.DateTimeField(null=False)
    port = models.PositiveIntegerField(null=False)
    key = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'node_ssh_configs'
    
    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'


class SSHConfigChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_ssh_config = models.ForeignKey('nodes.SSHConfig', on_delete=C, related_name='as_old_set', null=False)
    new_ssh_config = models.ForeignKey('nodes.SSHConfig', on_delete=C, related_name='as_new_set', null=False)
    comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_ssh_config_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentSSHConfig(models.Model):

    node = models.OneToOneField('nodes.Node', on_delete=C, related_name='current_ssh_config')
    effective_as_of = models.DateTimeField(null=False)
    port = models.PositiveIntegerField(null=False)
    key = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'node_current_ssh_configs'

    @staticmethod
    def refresh_materialized_view(*abs, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_ssh_configs')

    def __str__(self) -> str:
        return f'{self.node} [{self.timestamp}]'
