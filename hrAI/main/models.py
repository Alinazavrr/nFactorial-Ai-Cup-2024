from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('company', 'Company'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='candidate')
    is_company = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def is_candidate(self):
        return self.role == 'candidate'

    def is_company(self):
        return self.role == 'company'
# Модель для хранения информации о компаниях
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Связь с пользователями
    culture_values = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    social_media_links = models.JSONField(null=True, blank=True, default=dict)  # Ссылки на соцсети
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Модель для хранения информации о вакансиях
class JobPosting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

# Модель для хранения резюме кандидатов
class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Свя
    resume = models.FileField(upload_to='resumes/')
    applied_jobs = models.ManyToManyField(JobPosting, through='Application')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username}"

# Модель для хранения информации о заявках кандидатов на вакансии
class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired')
    ])
    rating = models.FloatField(default=0.0)  # Оценка кандидата
    feedback = models.TextField(blank=True)  # Обратная связь для HR о кандидате.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate} for {self.job_posting.title}"

# Модель для хранения обратной связи для кандидатов
class CandidateFeedback(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='feedback_to_candidate')
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback for {self.application.candidate} on {self.application.job_posting.title}"








# Модель для хранения анализа культурных ценностей компании
# class CulturalAnalysis(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cultural_analyses')
#     analysis = models.TextField()  # Анализ культурных ценностей
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Cultural Analysis for {self.company.name}"


# Модель для хранения результатов симуляций интервью
# class InterviewSimulation(models.Model):
#     candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='interview_simulations')
#     questions = models.JSONField(default=list)  # Вопросы интервью
#     answers = models.JSONField(default=dict)  # Ответы кандидата
#     evaluation = models.JSONField(default=dict)  # Оценка ответов
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Interview Simulation for {self.candidate}"

