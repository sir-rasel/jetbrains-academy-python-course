import json
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import HttpResponse


with open(settings.NEWS_JSON_PATH, 'r') as json_file:
    articles = json.load(json_file)


class ComingSoon(View):
    def get(self, request):
        return HttpResponse("Coming soon")


class MainView(View):
    def get(self, request):
        context = {'articles': articles}
        return render(
            request, 'news/publication.html', context
        )


class SingleView(View):
    def get(self, request, article_link):
        context = {}
        for article in articles:
            if article['link'] == int(article_link):
                context = {'article': article}

        return render(
            request, 'news/news_content.html', context
        )
