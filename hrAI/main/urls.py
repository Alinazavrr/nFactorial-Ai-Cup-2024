from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),

    # user autentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # upload files and quick results
    # path('upload_files/', upload_files, name='upload_files'),
    # path('results/', results, name='results'),

    # companies
    # path('companies/', CompanyListView.as_view(), name='company_list'),
    # path('companies/new/', CompanyCreateView.as_view(), name='company_create'),
    # path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    # path('companies/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company_update'),
    # path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),

    # job posting
    # path('companies/<int:company_id>/jobprofiles/new/', JobProfileCreateView.as_view(), name='jobprofile_create'),
    # path('jobprofiles/<int:pk>/edit/', JobProfileUpdateView.as_view(), name='jobprofile_update'),
    # path('jobprofiles/<int:pk>/', JobProfileDetailView.as_view(), name='jobprofile_detail'),
    # path('jobprofiles/<int:pk>/delete/', JobProfileDeleteView.as_view(), name='jobprofile_delete'),
]
