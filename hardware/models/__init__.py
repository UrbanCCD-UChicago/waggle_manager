from django.db.models.signals import post_save

from .component import Component
from .subsystem import Subsystem
from .instance import Instance
from .calibration import Calibration, CalibrationChange, CurrentCalibration
from .sensor import Sensor

post_save.connect(CurrentCalibration.refresh_materialized_view, sender=Calibration)
post_save.connect(CurrentCalibration.refresh_materialized_view, sender=CalibrationChange)
