from django.conf import settings
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class TelephonyIDs(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    effective_as_of = models.DateTimeField(null=False)
    sim_iccid = models.CharField(max_length=255, null=False)
    modem_imei = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'node_telephony_ids'
    
    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'


class TelephonyIDsChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_telephony_id = models.ForeignKey('nodes.TelephonyIDs', on_delete=C, related_name='as_old_set', null=False)
    new_telephony_id = models.ForeignKey('nodes.TelephonyIDs', on_delete=C, related_name='as_new_set', null=False)
    comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_telephony_id_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentTelephonyIDs(models.Model):

    node = models.OneToOneField('nodes.Node', on_delete=C, related_name='current_telephony_id')
    effective_as_of = models.DateTimeField(null=False)
    sim_iccid = models.CharField(max_length=255, null=False)
    modem_imei = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'node_current_telephony_ids'

    @staticmethod
    def refresh_materialized_view(*abs, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_telephony_ids')

    def __str__(self) -> str:
        return f'{self.node} [{self.timestamp}]'
