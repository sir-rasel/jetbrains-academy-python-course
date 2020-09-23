import json
from datetime import datetime
from django.shortcuts import render, redirect
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

class CreateNews(View):
    def get(self, request):
        return render(request, 'news/create_news.html')

    def post(self, request):
        news = dict()

        news['created'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        news['title'] = request.POST.get('title')
        news['text'] = request.POST.get('text')
        news['link'] = len(articles) + 1

        articles.append(news)

        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json.dump(articles, json_file)

        return redirect('main-page')