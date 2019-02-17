from django.db.models.signals import post_save

from .tag import Tag
from .node import Node
from .location import Location, LocationChange, CurrentLocation
from .description import Description, DescriptionChange, CurrentDescription
from .ssh_config import SSHConfig, SSHConfigChange, CurrentSSHConfig
from .ssl_cert import SSLCert, SSLCertChange, CurrentSSLCert
from .telephony import TelephonyIDs, TelephonyIDsChange, CurrentTelephonyIDs
from .state import State, StateChange, CurrentState
from .hardware import Hardware, HardwareChange, CurrentHardware
from .software import Software, SoftwareChange, CurrentSoftware

post_save.connect(CurrentLocation.refresh_materialized_view, sender=Location)
post_save.connect(CurrentLocation.refresh_materialized_view, sender=LocationChange)
post_save.connect(CurrentDescription.refresh_materialized_view, sender=Description)
post_save.connect(CurrentDescription.refresh_materialized_view, sender=DescriptionChange)
post_save.connect(CurrentSSHConfig.refresh_materialized_view, sender=SSHConfig)
post_save.connect(CurrentSSHConfig.refresh_materialized_view, sender=SSHConfigChange)
post_save.connect(CurrentSSLCert.refresh_materialized_view, sender=SSLCert)
post_save.connect(CurrentSSLCert.refresh_materialized_view, sender=SSLCertChange)
post_save.connect(CurrentTelephonyIDs.refresh_materialized_view, sender=TelephonyIDs)
post_save.connect(CurrentTelephonyIDs.refresh_materialized_view, sender=TelephonyIDsChange)
post_save.connect(CurrentState.refresh_materialized_view, sender=State)
post_save.connect(CurrentState.refresh_materialized_view, sender=StateChange)
post_save.connect(CurrentHardware.refresh_materialized_view, sender=Hardware)
post_save.connect(CurrentHardware.refresh_materialized_view, sender=HardwareChange)
post_save.connect(CurrentSoftware.refresh_materialized_view, sender=Software)
post_save.connect(CurrentSoftware.refresh_materialized_view, sender=SoftwareChange)
