from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from .models import Resume

class ResumePageView(View):
    def get(self, request):
        template_name = 'resume/resumePage.html'
        resume = Resume.objects.all()
        return render(request, template_name, {'resumes': resume})

class CreateResume(View):
    def post(self, request):
        username = request.user
        description = request.POST.get("description")
        if request.user.is_authenticated:
            post = Resume(author=username, description=description)
            post.save()
            return HttpResponseRedirect("/home")
        return HttpResponseForbidden()
