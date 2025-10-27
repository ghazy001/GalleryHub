from django.urls import path
from . import dashboard_views

urlpatterns = [
    # artwork
    path('artworks/', dashboard_views.artwork_list_view, name='dashboard_artwork_list'),
    path('artworks/create/', dashboard_views.artwork_create_view, name='dashboard_artwork_create'),
    path('artworks/<int:artwork_id>/edit/', dashboard_views.artwork_edit_view, name='dashboard_artwork_edit'),
    path('artworks/<int:artwork_id>/delete/', dashboard_views.artwork_delete_view, name='dashboard_artwork_delete'),
    path('artworks/stats/', dashboard_views.artwork_stats_view, name='dashboard_artwork_stats'),

    # feedback
    path('feedback/', dashboard_views.feedback_list_view, name='dashboard_feedback_list'),
    path('feedback/<int:feedback_id>/edit/', dashboard_views.feedback_edit_view, name='dashboard_feedback_edit'),
    path('feedback/<int:feedback_id>/delete/', dashboard_views.feedback_delete_view, name='dashboard_feedback_delete'),
    path('feedback/export/xlsx/', dashboard_views.feedback_export_excel_view, name='dashboard_feedback_export'),

]
