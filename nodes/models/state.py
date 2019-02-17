from django.conf import settings
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P
from djchoices import DjangoChoices, ChoiceItem


class States(DjangoChoices):
    being_built = ChoiceItem('being built')
    burn_in = ChoiceItem('burn in')
    testing = ChoiceItem('testing')
    in_storage = ChoiceItem('in storage')
    being_shipped_to_partner = ChoiceItem('being shipped to partner')
    in_storage_with_parter = ChoiceItem('in storage with partner')
    deployed = ChoiceItem('deployed')
    decomm_on_pole = ChoiceItem('decommissioned on pole')
    decomm_off_pole = ChoiceItem('decommissioned off pole')
    being_shipped_back = ChoiceItem('being shipped back home')


class State(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    effective_as_of = models.DateTimeField(null=False)
    state = models.CharField(max_length=255, null=False, choices=States.choices)

    class Meta:
        db_table = 'node_states'
    
    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'


class StateChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_state = models.ForeignKey('nodes.State', on_delete=C, related_name='as_old_set', null=False)
    new_state = models.ForeignKey('nodes.State', on_delete=C, related_name='as_new_set', null=False)
    comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_state_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentState(models.Model):

    node = models.OneToOneField('nodes.Node', on_delete=C, related_name='current_state')
    effective_as_of = models.DateTimeField(null=False)
    state = models.CharField(max_length=255, null=False, choices=States.choices)

    class Meta:
        managed = False
        db_table = 'node_current_states'

    @staticmethod
    def refresh_materialized_view(*abs, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_states')

    def __str__(self) -> str:
        return f'{self.node} [{self.timestamp}]'
