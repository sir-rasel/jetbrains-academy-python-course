from django.shortcuts import render
from django.views import View
from collections import deque
from django.views.generic.base import TemplateView
from math import inf

services_and_time = (('change_oil', 2), ('inflate_tires', 5), ('diagnostic', 30))
line_queue = {service[0]: deque() for service in services_and_time}
processed = 0

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

class ServiceView(View):
    def get(self, request, *args, **kwargs):
        service = kwargs['service']
        time = ServiceManagingOperation.minutes_to_wait(service)
        ticket = ServiceManagingOperation.get_ticket(service)
        return render(request, 'tickets/customer_queue.html', {'ticket': ticket, 'time': time})

class ServiceManagingOperation:
    @staticmethod
    def ticket_number():
        return processed + sum(len(line_queue[service[0]]) for service in services_and_time)

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
        line_queue[service].appendleft(ticket_number)
        return ticket_number
