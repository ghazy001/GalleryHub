from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.public_events_list_view, name='public_events_list'),
    path('events/<int:event_id>/', views.public_event_detail_view, name='public_event_detail'),
    # urls.py
    path('blog/', views.public_article_list_view, name='public_article_list'),
    path('blog/<int:article_id>/', views.public_article_detail_view, name='public_article_detail'),





]
