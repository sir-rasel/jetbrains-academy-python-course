from django.urls import path
from .views import ServiceTemplate

urlpatterns = [
    path('<str:operation>/', ServiceTemplate.as_view(), name="service"),

]