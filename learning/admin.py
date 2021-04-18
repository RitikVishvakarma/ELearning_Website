from django.contrib import admin
from .models import Contact, Videos, Subject, VideoComment

# Register your models here.
admin.site.register(Contact)
admin.site.register((Subject, Videos, VideoComment))
