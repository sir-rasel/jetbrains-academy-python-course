from django.shortcuts import render, redirect
from django.views import View
from collections import deque
from django.views.generic.base import TemplateView
from math import inf

services_and_time = (('change_oil', 2), ('inflate_tires', 5), ('diagnostic', 30))
line_queue = {service[0]: deque() for service in services_and_time}
ticket_no = 0
next_client = list()


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')

class ProcessingView(TemplateView):
    template_name = 'tickets/processing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines'] = {'Change oil': len(line_queue['change_oil']),
                            'Inflate tires': len(line_queue['inflate_tires']),
                            'Get diagnostic': len(line_queue['diagnostic'])}
        return context

    def post(self, request, *args, **kwargs):
        global next_client
        next_client = ServiceManagingOperation.choose_next_client()

        if next_client:
            line_queue[next_client[0]].popleft()
        
        return redirect('next')

class ServiceView(View):
    def get(self, request, *args, **kwargs):
        service = kwargs['service']
        time = ServiceManagingOperation.minutes_to_wait(service)
        ticket = ServiceManagingOperation.get_ticket(service)
        return render(request, 'tickets/customer_queue.html', {'ticket': ticket, 'time': time})

class NextClientView(View):
    def get(self, request, *args, **kwargs):
        massage = None
        if next_client:
            massage = f'Next ticket #{next_client[1]}'
        else:
            massage = 'Waiting for the next client'
        return render(request, 'tickets/next.html', {'massage': massage})

class ServiceManagingOperation:
    @staticmethod
    def choose_next_client():
        for service in line_queue.keys():
            if len(line_queue[service]) != 0:
                return [service, line_queue[service][0]]
        return list()

    @staticmethod
    def ticket_number():
        global ticket_no
        ticket_no += 1
        return ticket_no

    @staticmethod
    def minutes_to_wait(service):
        for i, (service_keyword, _) in enumerate(services_and_time):
            if service_keyword == service:
                index = i
                break
        else:
            return inf

        return sum(len(line_queue[services_and_time[i][0]]) * services_and_time[i][1] for i in range(index + 1))

    @staticmethod
    def get_ticket(service):
        ticket_number = ServiceManagingOperation.ticket_number()
        line_queue[service].append(ticket_number)
        return ticket_number
