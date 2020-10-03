from django.urls import path
from .views import *

urlpatterns = [
    path('new', CreateResume.as_view(), name='create-resume'),
]
