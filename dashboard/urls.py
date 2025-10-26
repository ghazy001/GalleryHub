from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),


# User management
    path('users/', views.user_list_view, name='dashboard_user_list'),
    path('users/<int:user_id>/ban/', views.user_ban_toggle_view, name='dashboard_user_ban_toggle'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='dashboard_user_delete'),

    # delegate event + place URLs to the events app
    path('', include('events.dashboard_urls')),


    # blog (articles / categories)
    path('', include('blog.dashboard_urls')),

    # gallery (artworks / feedback)
    path('', include('gallery.dashboard_urls')),


]
