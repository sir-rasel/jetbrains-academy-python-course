from django.urls import path
from .views import *

urlpatterns = [
    path('new', CreateVacancy.as_view(), name='create-vacancy'),
]
