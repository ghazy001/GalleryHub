
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from events.models import Event
from django.utils.timezone import now
from blog.models import Article, Category

def index(request):
    return render(request, 'main/index.html')


def public_events_list_view(request):
    events = (
        Event.objects
        .filter(is_published=True)
        .select_related('place')
        .order_by('start_date')
    )
    return render(request, 'main/events/public_events_list.html', {
        'events': events
    })


def public_event_detail_view(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related('place'),
        id=event_id,
        is_published=True
    )
    return render(request, 'main/events/public_event_detail.html', {
        'event': event
    })



def public_article_list_view(request):
    articles = (
        Article.objects
        .filter(is_published=True)
        .select_related('category', 'author')
        .order_by('-published_at')
    )
    return render(request, 'main/articles/public_blog_list.html', {
        'articles': articles
    })


def public_article_detail_view(request, article_id):
    article = get_object_or_404(
        Article.objects.select_related('category', 'author'),
        id=article_id,
        is_published=True
    )
    return render(request, 'main/articles/public_blog_detail.html', {
        'article': article
    })