from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django import forms
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menu/menu.html')

class MySignUpView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'menu/signup.html'

class MyLogInView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'menu/login.html'

class NewPostForm(forms.Form):
    description = forms.CharField(min_length=10, max_length=1024)

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        new_post_form = NewPostForm()
        return render(request, 'menu/profile.html', {'form': new_post_form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request_user = User.objects.filter(username=request.user.username)[0]
            if request_user.is_staff:
                return redirect('/vacancy/new')
            else:
                return redirect('/resume/new')
        else:
            raise PermissionDenied
