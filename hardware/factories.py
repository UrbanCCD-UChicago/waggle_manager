import factory
import pytz
from django.contrib.auth import get_user_model

from .models import Component, Instance, Calibration, CalibrationChange


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()


class ComponentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Component
    
    name = factory.Faker('itin')
    manufacturer = factory.Faker('company')
    version = factory.Faker('isbn10')


class InstanceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Instance

    component = factory.SubFactory(ComponentFactory)
    uid = factory.Faker('ean13')


class CalibrationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Calibration
    
    instance = factory.SubFactory(InstanceFactory)
    value = factory.Faker('name')
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)


class CalibrationChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = CalibrationChange
    
    instance = factory.SubFactory(InstanceFactory)
    old_calibration = factory.SubFactory(CalibrationFactory)
    new_calibration = factory.SubFactory(CalibrationFactory)
    user = factory.SubFactory(UserFactory)
