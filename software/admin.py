from django.contrib import admin
from .models import *


admin.site.register(Software)
admin.site.register(DeprecatesSoftware)
admin.site.register(SoftwareRequires)
admin.site.register(ImageIncludes)
admin.site.register(NeedsHardware)
admin.site.register(ProvidesHardware)
admin.site.register(RecognizesHardware)
