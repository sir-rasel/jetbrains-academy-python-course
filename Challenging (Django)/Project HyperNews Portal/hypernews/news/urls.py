from django.urls import path, re_path
from .views import MainView, SingleView, CreateNews

urlpatterns = [
    path('', MainView.as_view(), name='main-page'),
    path('create/', CreateNews.as_view(), name='create-page'),
    path('<int:article_link>/', SingleView.as_view(), name='news-page'),
]
