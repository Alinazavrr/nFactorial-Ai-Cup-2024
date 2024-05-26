# forms.py

from django import forms
from .models import Company, JobPosting, Candidate, CustomUser


class RoleSelectionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        widgets = {
            'role': forms.RadioSelect
        }
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'culture_values', 'website', 'social_media_links']

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['resume']

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
