# hr/forms.py
from django import forms
from .models import Company, JobPosting, Candidate, Application


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description']

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'company']

