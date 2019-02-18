from django.conf import settings
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class SSLCert(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    effective_as_of = models.DateTimeField(null=False)
    ssl_cert = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'node_ssl_certs'
    
    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'


class SSLCertChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_ssl_cert = models.ForeignKey('nodes.SSLCert', on_delete=C, related_name='as_old_set', null=False)
    new_ssl_cert = models.ForeignKey('nodes.SSLCert', on_delete=C, related_name='as_new_set', null=False)
    comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_ssl_cert_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentSSLCert(models.Model):

    node = models.OneToOneField('nodes.Node', on_delete=C, related_name='current_ssl_cert')
    effective_as_of = models.DateTimeField(null=False)
    ssl_cert = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'node_current_ssl_certs'

    @staticmethod
    def create_materialized_view():
        return """
        CREATE MATERIALIZED VIEW node_current_ssl_certs AS
            SELECT id, node_id, ssl_cert, effective_as_of
            FROM node_ssl_certs
            WHERE id NOT IN (
                SELECT DISTINCT old_ssl_cert_id
                FROM node_ssl_cert_changes
            )
        """

    @staticmethod
    def refresh_materialized_view(*args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_ssl_certs')

    def __str__(self) -> str:
        return f'{self.node} [{self.timestamp}]'
