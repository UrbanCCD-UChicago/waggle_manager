import factory

from .models import Software


class SoftwareFactory(factory.DjangoModelFactory):
    class Meta:
        model = Software
    
    name = factory.Faker('bs')
    version = factory.Faker('isbn10')
    type = 'plugin'
    source_url = factory.Faker('uri')
