from django.contrib import admin
from home.models import Assignment, Submission
# Register your models here.

admin.site.register((Assignment, Submission))