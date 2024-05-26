# from django
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction

# from this app
from .models import Company, JobPosting, Application, CandidateFeedback, Candidate
from .utils import extract_text_from_pdf, evaluate_candidate, parse_evaluation
from .forms import CompanyForm, JobPostingForm, CandidateForm, ResumeUploadForm, RoleSelectionForm



# user autentication
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

# home page
class HomePageView(TemplateView):
    template_name = 'main/home_page.html'





class CandidateFeedbackListView(LoginRequiredMixin, ListView):
    model = CandidateFeedback
    template_name = 'main/candidate_feedback_list.html'
    context_object_name = 'feedback_list'

    def get_queryset(self):
        # Get the candidate object for the logged-in user
        candidate = get_object_or_404(Candidate, user=self.request.user.custom_user)
        # Return the feedbacks related to this candidate
        return CandidateFeedback.objects.filter(application__candidate=candidate)
    
class CompanyApplicationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Application
    template_name = 'main/company_applications_list.html'
    context_object_name = 'applications_list'

    def test_func(self):
        return self.request.user.custom_user.is_company()

    def get_queryset(self):
        company = get_object_or_404(Company, user=self.request.user.custom_user)
        queryset = Application.objects.filter(job_posting__company=company)
        
        # Check for sorting parameter
        sort_by = self.request.GET.get('sort', 'created_at')
        if sort_by == 'rating':
            queryset = queryset.order_by('-rating')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset


class JobPostingApplicationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Application
    template_name = 'main/jobposting_applications_list.html'
    context_object_name = 'applications_list'

    def test_func(self):
        job_posting = get_object_or_404(JobPosting, id=self.kwargs['job_id'])
        return job_posting.company.user == self.request.user.custom_user

    def get_queryset(self):
        job_posting = get_object_or_404(JobPosting, id=self.kwargs['job_id'])
        queryset = Application.objects.filter(job_posting=job_posting)
        
        # Check for sorting parameter
        sort_by = self.request.GET.get('sort', 'created_at')
        if sort_by == 'rating':
            queryset = queryset.order_by('-rating')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset



# COMPANY

class CompanyJobPostingsListView(LoginRequiredMixin, ListView):
    model = JobPosting
    template_name = 'main/company_job_postings_list.html'
    context_object_name = 'job_postings_list'

    def get_queryset(self):
        user = self.request.user
        if user.custom_user.is_company():
            queryset = JobPosting.objects.filter(company=user.custom_user.company)
            
            sort_by = self.request.GET.get('sort', 'created_at')
            if sort_by not in ['created_at', 'title']:
                sort_by = 'created_at'

            return queryset.order_by(sort_by)
        else:
            return JobPosting.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort', 'created_at')
        return context

class CompanyListView(ListView):
    model = Company
    template_name = 'company/company_list.html'

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['job_postings'] = JobPosting.objects.filter(company=company).order_by('created_at')
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('company-list')


    def form_valid(self, form):
        form.instance.user = self.request.user.custom_user
        return super().form_valid(form)

class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'

    def test_func(self):
        company = self.get_object()
        return self.request.user.custom_user.is_company() and company.user == self.request.user.custom_user

class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Company
    template_name = 'company/company_confirm_delete.html'
    success_url = reverse_lazy('company-list')

    def test_func(self):
        company = self.get_object()
        return self.request.user.custom_user == company.user



# job posting

class JobPostingListView(ListView):
    model = JobPosting
    template_name = 'jobposting/jobposting_list.html'

class JobPostingDetailView(DetailView):
    model = JobPosting
    template_name = 'jobposting/jobposting_detail.html'
    context_object_name = 'job_posting'

class JobPostingCreateView(LoginRequiredMixin, CreateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'jobposting/jobposting_form.html'
    success_url = reverse_lazy('jobposting-list')

    def form_valid(self, form):
        form.instance.company = self.request.user.custom_user.company
        return super().form_valid(form)

class JobPostingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'jobposting/jobposting_form.html'
    success_url = reverse_lazy('jobposting-list')

    def test_func(self):
        jobposting = self.get_object()
        return self.request.user.custom_user == jobposting.company.user

class JobPostingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobPosting
    template_name = 'jobposting/jobposting_confirm_delete.html'
    success_url = reverse_lazy('jobposting-list')

    def test_func(self):
        jobposting = self.get_object()
        return self.request.user.custom_user == jobposting.company.user




# Candidate

class CandidateListView(ListView):
    model = Candidate
    template_name = 'candidate/candidate_list.html'

class CandidateDetailView(DetailView):
    model = Candidate
    template_name = 'candidate/candidate_detail.html'

class CandidateCreateView(LoginRequiredMixin, CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'candidate/candidate_form.html'
    success_url = reverse_lazy('candidate-list')

    def form_valid(self, form):
        form.instance.user = self.request.user.custom_user
        return super().form_valid(form)

class CandidateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'candidate/candidate_form.html'
    success_url = reverse_lazy('candidate-list')

    def test_func(self):
        candidate = self.get_object()
        return self.request.user.custom_user.is_candidate() and candidate.user == self.request.user.custom_user

class CandidateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Candidate
    template_name = 'candidate/candidate_confirm_delete.html'
    success_url = reverse_lazy('candidate-list')

    def test_func(self):
        candidate = self.get_object()
        return self.request.user.custom_user == candidate.user



# upload files and quick results
# def upload_files(request):
#     try:
#         company = request.user.company
#     except Company.DoesNotExist:
#         return redirect('company_create')

#     if request.method == 'POST':
#         job_profile = JobProfile.objects.create(
#             company=company,
#             position=request.POST['position'],
#             description=request.POST['description']
#         )
        
#         for file in request.FILES.getlist('resumes'):
#             candidate = Candidate.objects.create(
#                 job_profile=job_profile,
#                 name=file.name,
#                 resume=file
#             )
#             resume_text = extract_text_from_pdf(candidate.resume.path)
#             evaluation = evaluate_candidate(job_profile.description, resume_text)
#             candidate.score, candidate.explanation = parse_evaluation(evaluation)
#             candidate.passed = candidate.score and candidate.score >= 70  # Example threshold
#             candidate.save()

#         return redirect('results')
#     return render(request, 'main/upload.html')


# def results(request):
#     try:
#         company = request.user.company
#     except Company.DoesNotExist:
#         return redirect('company_create')

#     candidates = Candidate.objects.filter(job_profile__company=company)
#     return render(request, 'main/results.html', {'candidates': candidates})



class ApplyForJobView(LoginRequiredMixin, FormView):
    template_name = 'main/apply_for_job.html'
    success_url = reverse_lazy('jobposting-list')  # Вы можете изменить это на нужный URL

    def dispatch(self, request, *args, **kwargs):
        self.job_posting = get_object_or_404(JobPosting, id=kwargs['job_id'])
        self.candidate = get_object_or_404(Candidate, user=request.user.custom_user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Проверим, есть ли у кандидата резюме
        if not self.candidate.resume:
            messages.error(request, 'You need to upload a resume before applying for a job.')
            return redirect('candidate-profile')  # Перенаправить на страницу профиля кандидата для загрузки резюме
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        resume_text = extract_text_from_pdf(self.candidate.resume.path)

        job_profile = self.job_posting.description
        company_culture = self.job_posting.company.culture_values

        evaluation_text = evaluate_candidate(job_profile, company_culture, resume_text)
        company_score, company_explanation, candidate_feedback = parse_evaluation(evaluation_text)

        if company_score is not None:
            with transaction.atomic():
                application = Application.objects.create(
                    candidate=self.candidate,
                    job_posting=self.job_posting,
                    status='under_review',
                    rating=company_score,
                    feedback=company_explanation
                )

                CandidateFeedback.objects.create(
                    application=application,
                    feedback=candidate_feedback
                )

            messages.success(self.request, 'Your application has been submitted successfully.')
        else:
            messages.error(self.request, 'There was an error processing your application. Please try again.')

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_posting'] = self.job_posting
        return context