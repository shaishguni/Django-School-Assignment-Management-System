from django.forms import ModelForm
from home import models
from django.contrib.auth.models import User
from django import forms
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField

class AssignmentForm(ModelForm):
    upload = forms.FileField(
        required=False,
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    class Meta:
        model = models.Assignment
        fields = ['title', 'upload', 'due_date']


# class SubmissionForm(ModelForm):
#     upload = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))

#     class Meta:
#         model = models.Submission
#         fields = ['upload']






class SubmissionForm(ModelForm):
    descprition = forms.CharField() 
    class Meta:
        model = models.Submission
        fields = ('upload', 'descprition')




class AssignmentSearchForm(forms.Form):
    q = forms.CharField()

    class Meta:
        fields = "q"
        errorlist = {
            'q': '',
        }


class SubmissionSearchForm(forms.Form):
    q = forms.CharField()

    class Meta:
        fields = "q"


class GradeForm(forms.Form):
    grade = forms.CharField()

    class Meta:
        fields = ['grade']


class FeedbackForm(forms.Form):
    feedback = forms.CharField()
    
    class Meta:
        fields = ['feedback']


class PassForm(forms.Form):
    passcode = forms.CharField()

    class Meta:
        fields = "passcode"

