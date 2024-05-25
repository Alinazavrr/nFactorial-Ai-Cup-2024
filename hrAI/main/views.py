# from django
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView 
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# from this app
# from .models import Company, JobPosting, Candidate
# from .forms import CompanyForm, JobPostingForm





# user autentication
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home_page')

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')



# home page
class HomePageView(TemplateView):
    template_name = 'main/home_page.html'



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


# job profile CRUD

# class JobProfileCreateView(CreateView):
#     model = JobProfile
#     form_class = JobProfileForm
#     template_name = 'jobprofile_create.html'

#     def form_valid(self, form):
#         form.instance.company = get_object_or_404(Company, id=self.kwargs['company_id'])
#         response = super().form_valid(form)
#         if self.request.FILES.getlist('resumes'):
#             self.object.evaluate_candidates(self.request.FILES.getlist('resumes'))
#         return response

#     def get_success_url(self):
#         return reverse_lazy('company_detail', kwargs={'pk': self.object.company.id})

# class JobProfileUpdateView(UpdateView):
#     model = JobProfile
#     form_class = JobProfileForm
#     template_name = 'jobprofile_update.html'

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         if self.request.FILES.getlist('resumes'):
#             self.object.evaluate_candidates(self.request.FILES.getlist('resumes'))
#         return response

#     def get_success_url(self):
#         return reverse('jobprofile_detail', kwargs={'pk': self.object.pk})

# class JobProfileDetailView(DetailView):
#     model = JobProfile
#     template_name = 'jobprofile_detail.html'

# class JobProfileDeleteView(DeleteView):
#     model = JobProfile
#     template_name = 'jobprofile_confirm_delete.html'

#     def get_success_url(self):
#         return reverse_lazy('company_detail', kwargs={'pk': self.object.company.id})



# company CRUD
# class CompanyCreateView(LoginRequiredMixin, CreateView):
#     model = Company
#     form_class = CompanyForm
#     template_name = 'main/company_form.html'
#     success_url = reverse_lazy('company_list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

# class CompanyListView(LoginRequiredMixin, ListView):
#     model = Company
#     template_name = 'main/company_list.html'
#     context_object_name = 'companies'

#     def get_queryset(self):
#         return Company.objects.filter(user=self.request.user)

# class CompanyUpdateView(LoginRequiredMixin, UpdateView):
#     model = Company
#     form_class = CompanyForm
#     template_name = 'main/company_form.html'
#     success_url = reverse_lazy('company_list')

#     def get_queryset(self):
#         return Company.objects.filter(user=self.request.user)
    
# class CompanyDetailView(LoginRequiredMixin, DetailView):
#     model = Company
#     template_name = 'company_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         company = self.get_object()
#         context['company'] = company
#         context['jobprofiles'] = JobProfile.objects.filter(company=company)
#         return context
    
# class CompanyDeleteView(LoginRequiredMixin, View):
#     def post(self, request, pk, *args, **kwargs):
#         company = get_object_or_404(Company, pk=pk, user=request.user)
#         company.delete()
#         return redirect('company_list')