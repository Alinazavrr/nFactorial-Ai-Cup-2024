from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('job/<int:job_id>/apply/', ApplyForJobView.as_view(), name='apply-for-job'),
    path('feedback/', CandidateFeedbackListView.as_view(), name='candidate-feedback-list'),
    path('company/applications/', CompanyApplicationsListView.as_view(), name='company-applications-list'),
    path('job/<int:job_id>/applications/', JobPostingApplicationsListView.as_view(), name='jobposting-applications-list'),

    # user autentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('companies/new/', CompanyCreateView.as_view(), name='company-create'),
    path('companies/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company-update'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete'),
    path('company/job_postings/', CompanyJobPostingsListView.as_view(), name='company-job-postings-list'),

    path('jobpostings/', JobPostingListView.as_view(), name='jobposting-list'),
    path('jobpostings/<int:pk>/', JobPostingDetailView.as_view(), name='jobposting-detail'),
    path('jobpostings/new/', JobPostingCreateView.as_view(), name='jobposting-create'),
    path('jobpostings/<int:pk>/edit/', JobPostingUpdateView.as_view(), name='jobposting-update'),
    path('jobpostings/<int:pk>/delete/', JobPostingDeleteView.as_view(), name='jobposting-delete'),

    path('candidates/', CandidateListView.as_view(), name='candidate-list'),
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('candidates/new/', CandidateCreateView.as_view(), name='candidate-create'),
    path('candidates/<int:pk>/edit/', CandidateUpdateView.as_view(), name='candidate-update'),
    path('candidates/<int:pk>/delete/', CandidateDeleteView.as_view(), name='candidate-delete'),
]
