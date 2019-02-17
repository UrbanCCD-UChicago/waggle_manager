import factory
import pytz
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from hardware.factories import InstanceFactory
from software.factories import SoftwareFactory as SoftwareSoftwareFactory
from .models import Node, Description, DescriptionChange, \
    Location, LocationChange, SSHConfig, SSHConfigChange, \
    SSLCert, SSLCertChange, State, StateChange, \
    TelephonyIDs, TelephonyIDsChange, Hardware, HardwareChange, \
    Software, SoftwareChange


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()


class NodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Node
    
    id = factory.Faker('uuid4', cast_to=str)
    vsn = factory.Faker('uuid4', cast_to=str)


class DescriptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Description

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    description = factory.Faker('text', max_nb_chars=100)


class DescriptionChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = DescriptionChange

    node = factory.SubFactory(NodeFactory)
    old_description = factory.SubFactory(DescriptionFactory)
    new_description = factory.SubFactory(DescriptionFactory)
    user = factory.SubFactory(UserFactory)


class LocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Location

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    location = Point(1, 1)


class LocationChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = LocationChange

    node = factory.SubFactory(NodeFactory)
    old_location = factory.SubFactory(LocationFactory)
    new_location = factory.SubFactory(LocationFactory)
    user = factory.SubFactory(UserFactory)


class SSHConfigFactory(factory.DjangoModelFactory):
    class Meta:
        model = SSHConfig

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    port = factory.Faker('pyint')
    key = factory.Faker('text', max_nb_chars=100)


class SSHConfigChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = SSHConfigChange

    node = factory.SubFactory(NodeFactory)
    old_ssh_config = factory.SubFactory(SSHConfigFactory)
    new_ssh_config = factory.SubFactory(SSHConfigFactory)
    user = factory.SubFactory(UserFactory)


class SSLCertFactory(factory.DjangoModelFactory):
    class Meta:
        model = SSLCert

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    ssl_cert = factory.Faker('text', max_nb_chars=100)


class SSLCertChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = SSLCertChange

    node = factory.SubFactory(NodeFactory)
    old_ssl_cert = factory.SubFactory(SSLCertFactory)
    new_ssl_cert = factory.SubFactory(SSLCertFactory)
    user = factory.SubFactory(UserFactory)


class StateFactory(factory.DjangoModelFactory):
    class Meta:
        model = State

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    state = 'being built'


class StateChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = StateChange

    node = factory.SubFactory(NodeFactory)
    old_state = factory.SubFactory(StateFactory)
    new_state = factory.SubFactory(StateFactory)
    user = factory.SubFactory(UserFactory)


class TelephonyIDsFactory(factory.DjangoModelFactory):
    class Meta:
        model = TelephonyIDs

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    sim_iccid = factory.Faker('text', max_nb_chars=100)
    modem_imei = factory.Faker('text', max_nb_chars=100)


class TelephonyIDsChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = TelephonyIDsChange

    node = factory.SubFactory(NodeFactory)
    old_telephony_id = factory.SubFactory(TelephonyIDsFactory)
    new_telephony_id = factory.SubFactory(TelephonyIDsFactory)
    user = factory.SubFactory(UserFactory)


class HardwareFactory(factory.DjangoModelFactory):
    class Meta:
        model = Hardware

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    instance = factory.SubFactory(InstanceFactory)


class HardwareChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = HardwareChange

    node = factory.SubFactory(NodeFactory)
    old_instance = factory.SubFactory(HardwareFactory)
    new_instance = factory.SubFactory(HardwareFactory)
    user = factory.SubFactory(UserFactory)


class SoftwareFactory(factory.DjangoModelFactory):
    class Meta:
        model = Software

    node = factory.SubFactory(NodeFactory)
    effective_as_of = factory.Faker('date_time', tzinfo=pytz.UTC)
    software = factory.SubFactory(SoftwareSoftwareFactory)


class SoftwareChangeFactory(factory.DjangoModelFactory):
    class Meta:
        model = SoftwareChange

    node = factory.SubFactory(NodeFactory)
    old_software = factory.SubFactory(SoftwareFactory)
    new_software = factory.SubFactory(SoftwareFactory)
    user = factory.SubFactory(UserFactory)
