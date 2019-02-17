from django.db import models
from django.db.models import PROTECT as P


class ImageIncludes(models.Model):

    image = models.ForeignKey('software.Software', on_delete=P, related_name='includes_set', null=False)
    included_software = models.ForeignKey('software.Software', on_delete=P, related_name='included_in_image_set', null=False)

    class Meta:
        db_table = 'image_icludes_software'
        unique_together = [
            ('image', 'included_software')
        ]

    def __str__(self) -> str:
        return f'{self.image} -> {self.included_software}'
