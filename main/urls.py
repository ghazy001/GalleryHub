from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.public_events_list_view, name='public_events_list'),
    path('events/<int:event_id>/', views.public_event_detail_view, name='public_event_detail'),
    # urls.py
    path('blog/', views.public_article_list_view, name='public_article_list'),
    path('blog/<int:article_id>/', views.public_article_detail_view, name='public_article_detail'),

    path('artworks/', views.public_artwork_list_view, name='public_artwork_list'),
    path('artworks/<int:artwork_id>/', views.public_artwork_detail_view, name='public_artwork_detail'),

    path('workshops', views.public_workshop_list_view, name='public_workshop_list'),
    path('workshops/<int:workshop_id>/', views.public_workshop_detail_view, name='public_workshop_detail'),

    path("ai-image/", views.ai_image_generator_page, name="ai_image_generator"),
    path("ai-bg-remove/", views.ai_background_remover_page, name="ai_background_remover"),
    path("ai-photo-editor/", views.ai_photo_editor_page, name="ai_photo_editor"),



]
