import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def upload_profile_to(instance,filename):
	return f'profile_picture/{instance.user.username}/{filename}'

def upload_cover_to(instance,filename):
	return f'coverImage/{instance.user.username}/{filename}'

class Profile(models.Model):
    role_choice = (('Teacher', 'Teacher'), ('Student', 'Student'))
    role_choice_section = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))
    subject_choice = (('Computer', 'Computer') , ('Nepali' , 'Nepali') , ('Social', 'Social') , ('English', 'English'), ('OBTE', 'OBTE') , ('Health', 'Health') , ('Opt Maths', 'Opt Maths'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=role_choice, default='Teacher')
    roll_number = models.CharField(max_length=12, blank=True, null=True)
    Class = models.IntegerField(null=True, blank=True)
    section =models.CharField(max_length=100, null=True, blank=True, choices=role_choice_section)
    subject = models.CharField(max_length=100, null=True, blank=True, choices=subject_choice)
    number = models.BigIntegerField(null=True, blank=True)
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username 


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    seen = models.BooleanField(default=False)




class Notification_general(models.Model):
    title = models.CharField(blank=True, null=True, max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=500)
    files =models.ImageField(upload_to='notification/', null=True, blank=True)
    parents_choice = (('Yes', 'Yes'), ('No', 'No'))
    seen = models.BooleanField(default=False)
    parents_avaviality = models.CharField(choices=parents_choice, max_length=6, null=True)