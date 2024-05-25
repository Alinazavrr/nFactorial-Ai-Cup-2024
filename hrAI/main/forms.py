# hr/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Company, JobProfile

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description']

class JobProfileForm(forms.ModelForm):
    class Meta:
        model = JobProfile
        fields = ['position', 'description']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }