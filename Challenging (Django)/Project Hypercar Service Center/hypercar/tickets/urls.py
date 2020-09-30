from django.urls import path
from .views import ServiceView

urlpatterns = [
    path('<str:service>/', ServiceView.as_view(), name="service"),

]