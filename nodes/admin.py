from django.contrib import admin
from .models import *

from django.db.models.signals import post_save

admin.site.register(Node)
admin.site.register(Tag)
admin.site.register(Location)
admin.site.register(LocationChange)
admin.site.register(Description)
admin.site.register(DescriptionChange)
admin.site.register(SSHConfig)
admin.site.register(SSHConfigChange)
admin.site.register(SSLCert)
admin.site.register(SSLCertChange)
admin.site.register(TelephonyIDs)
admin.site.register(TelephonyIDsChange)
admin.site.register(State)
admin.site.register(StateChange)
admin.site.register(Hardware)
admin.site.register(HardwareChange)
admin.site.register(Software)
admin.site.register(SoftwareChange)
