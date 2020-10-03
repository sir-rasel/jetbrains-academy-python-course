from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from .models import Vacancy

class VacancyPageView(View):
    def get(self, request):
        template_name = 'vacancy/vacancyPage.html'
        vacancy = Vacancy.objects.all()
        return render(request, template_name, {'vacancies': vacancy})

class CreateVacancy(View):
    def post(self, request):
        username = request.user
        description = request.POST.get("description")
        if request.user.is_staff:
            post = Vacancy(author=username, description=description)
            post.save()
            return HttpResponseRedirect("/home")
        return HttpResponseForbidden()
