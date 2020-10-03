from django.urls import path
from .views import MenuView

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),
]
