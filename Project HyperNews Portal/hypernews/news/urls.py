from django.urls import path, re_path
from .views import MainView, SingleView

urlpatterns = [
    path('', MainView.as_view()),
    path('<str:article_link>', SingleView.as_view()),
]
