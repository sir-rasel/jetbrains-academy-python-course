from django.shortcuts import render
from django.views import View
from collections import deque
from django.views.generic.base import TemplateView

class WelcomeView(View):    
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')

class ServiceTemplate(TemplateView):
    template_name = 'tickets/customer_queue.html'
    que = {'oil': deque(), 'tires': deque(), 'diagnostic': deque()}
    number = None
    time = None
    def get_context_data(self, **kwargs):
        operation = super().get_context_data(**kwargs)['operation']
        if operation == 'change_oil':
            self.time = len(self.que['oil']) * 2
            self.que['oil'].append('customer')
            self.number = len(self.que['oil'])
        elif operation == 'inflate_tires':
            self.time = len(self.que['oil']) * 2 + len(self.que['tires']) * 5
            self.que['tires'].append('another_one')
            self.number = len(self.que['tires'])
        elif operation == 'diagnostic':
            self.time = len(self.que['oil']) * 2 + len(self.que['tires']) * 5 + len(self.que['diagnostic']) * 30
            self.que['diagnostic'].append('and_another_one')
            self.number = len(self.que['diagnostic'])
        else:
            pass

        if self.number is None:
            return "Sorry, you've chosen wrong option"
        info = {'number': self.number, 'time': self.time}
        return info
