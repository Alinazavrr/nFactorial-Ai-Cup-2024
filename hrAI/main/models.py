from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class JobProfile(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.company.name} - {self.position}"

    def evaluate_candidates(self):
        from .utils import extract_text_from_pdf, evaluate_candidate, parse_evaluation
        candidates = self.candidate_set.all()
        for candidate in candidates:
            resume_text = extract_text_from_pdf(candidate.resume.path)
            evaluation_text = evaluate_candidate(self.description, resume_text)
            score, explanation = parse_evaluation(evaluation_text)
            candidate.passed = score > 70
            candidate.explanation = explanation
            candidate.save()

class Candidate(models.Model):
    job_profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')
    score = models.FloatField(null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name