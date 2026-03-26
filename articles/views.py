from django.shortcuts import render
from .models import Article


def article_list(request):
    """Отображает список всех статей"""
    # Получаем все статьи с предварительной загрузкой связанных данных
    articles = Article.objects.all().prefetch_related('scopes__tag')
    return render(request, 'articles/article_list.html', {'articles': articles})
