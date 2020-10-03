"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from vacancy.views import VacancyPageView
from resume.views import ResumePageView
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView
from menu.views import *
from vacancy.views import *
from resume.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
    path('home/', HomePageView.as_view(), name='home'),
    path('home', RedirectView.as_view(url='home/')),
    path('vacancies/', VacancyPageView.as_view(), name='vacancies'),
    path('vacancy/', include('vacancy.urls')),
    path('resumes/', ResumePageView.as_view(), name='resumes'),
    path('resume/', include('resume.urls')),
    path('signup', MySignUpView.as_view(), name='signup'),
    path('login', MyLogInView.as_view(), name='login'),
    path('login/', RedirectView.as_view(url='/login')),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('logout/', LogoutView.as_view()),
]
