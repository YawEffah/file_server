from django.contrib import admin

from .models import *

admin.site.register(UploadedFile)
admin.site.register(Email)
admin.site.register(Download)
