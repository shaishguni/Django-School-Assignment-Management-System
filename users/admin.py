from django.contrib import admin
from .models import Profile, Notification, Notification_general
# Register your models here.
admin.site.register((Profile, Notification, Notification_general))