from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.db import models, connection
from django.db.models import CASCADE as C
from django.db.models import PROTECT as P


class Location(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    effective_as_of = models.DateTimeField(null=False)
    location = PointField(null=False)
    altitude = models.FloatField(null=True, default=None, blank=True)
    elevation = models.FloatField(null=True, default=None, blank=True)
    orientation = JSONField(null=True, default=None, blank=True)

    class Meta:
        db_table = 'node_locations'
    
    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'


class LocationChange(models.Model):

    node = models.ForeignKey('nodes.Node', on_delete=C, null=False)
    old_location = models.ForeignKey('nodes.Location', on_delete=C, related_name='as_old_set', null=False)
    new_location = models.ForeignKey('nodes.Location', on_delete=C, related_name='as_new_set', null=False)
    comment = models.TextField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=P, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'node_location_changes'

    def __str__(self) -> str:
        return f'{self.node} [{self.created_on}]'


class CurrentLocation(models.Model):

    node = models.OneToOneField('nodes.Node', on_delete=C, related_name='current_location')
    effective_as_of = models.DateTimeField(null=False)
    location = PointField(null=False)
    altitude = models.FloatField(null=True, default=None, blank=True)
    elevation = models.FloatField(null=True, default=None, blank=True)
    orientation = JSONField(null=True, default=None, blank=True)

    class Meta:
        managed = False
        db_table = 'node_current_locations'

    @staticmethod
    def refresh_materialized_view(*abs, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                'REFRESH MATERIALIZED VIEW node_current_locations')

    def __str__(self) -> str:
        return f'{self.node} [{self.effective_as_of}]'
