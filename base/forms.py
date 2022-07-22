from django import forms
from django.forms import ModelForm
from base.models import Course, Participant

class DateWidg(forms.DateInput):
    input_type = 'date'


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['contact_email']


class CourseCreationForm(ModelForm):

    start_date = forms.DateField(widget=DateWidg)
    end_date = forms.DateField(widget=DateWidg)
    
    class Meta:
        model = Course
        exclude =['host']
