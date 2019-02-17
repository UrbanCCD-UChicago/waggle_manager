from django.contrib import admin
from .models import *

admin.site.register(Component)
admin.site.register(Subsystem)
admin.site.register(Instance)
admin.site.register(Calibration)
admin.site.register(CalibrationChange)
admin.site.register(CurrentCalibration)
admin.site.register(Sensor)
