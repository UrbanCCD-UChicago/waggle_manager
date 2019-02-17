from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class Software(models.Model):

    class Types(DjangoChoices):
        image = ChoiceItem('image')
        firmware = ChoiceItem('firmware')
        driver = ChoiceItem('driver')
        plugin = ChoiceItem('plugin')
    
    name = models.CharField(max_length=255, null=False)
    version = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=255, choices=Types.choices)
    source_url = models.CharField(max_length=255, null=False)
    documentation = models.CharField(max_length=255, null=True, default=None, blank=True)
    description = models.CharField(max_length=255, null=True, default=None, blank=True)

    class Meta:
        db_table = 'software_software'
        verbose_name_plural = 'Software'
        unique_together = [
            ('name', 'version', 'type')
        ]

    def __str__(self) -> str:
        return f'{self.name} {self.version} [{self.type}]'
