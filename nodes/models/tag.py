from django.db import models, connection
from django.template.defaultfilters import slugify


class Tag(models.Model):

    name = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        db_table = 'node_tags'
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
