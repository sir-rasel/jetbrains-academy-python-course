from django.shortcuts import render
from django.views import View

# Create your views here.
class WelcomeView(View):    
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')
