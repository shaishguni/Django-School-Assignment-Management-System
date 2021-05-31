from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
import os






class Assignment(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='assignments/', null=True, default="No file uploaded")

    due_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    # subject = models.ForeignKey(Profile.subject, on_delete=models.CASCADE,)

    descprition = models.CharField(null=True, blank=True, max_length=1000)
    submmetted_by = models.ManyToManyField(User, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    def extension_ass(self):
        extension = os.path.splitext(self.upload.name)[1]
        return extension

    def __str__(self):
        return self.user.username + " created " + self.title



class Submission(models.Model):
    upload = models.FileField(upload_to='submissions/', default="No file uploaded")
    submitted_at = models.DateField(auto_now=True)
    descprition = models.CharField(null=True, blank=True, max_length=1000)
    last_updated = models.DateField(auto_now=True)
    assignment = models.ForeignKey(
        'Assignment',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    def extension_sub(self):
        extension = os.path.splitext(self.upload.name)[1]
        return extension

    grade = models.CharField(max_length=100, null=True, blank=True, default="No grade yet")
    feedback = models.CharField(max_length=255, null=True, blank=True, default="No feedback yet")
    def __str__(self):
        return self.user.username + " submmitted " + self.assignment.title



