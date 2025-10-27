# events/dashboard_urls.py
from django.urls import path
from . import dashboard_views

urlpatterns = [
    # places CRUD
    path('places/', dashboard_views.place_list_view, name='dashboard_place_list'),
    path('places/create/', dashboard_views.place_create_view, name='dashboard_place_create'),
    path('places/<int:place_id>/edit/', dashboard_views.place_edit_view, name='dashboard_place_edit'),
    path('places/<int:place_id>/delete/', dashboard_views.place_delete_view, name='dashboard_place_delete'),
    path('places/export/xlsx/', dashboard_views.place_export_excel_view, name='dashboard_place_export'),

    # events CRUD
    path('events/', dashboard_views.event_list_view, name='dashboard_event_list'),
    path('events/create/', dashboard_views.event_create_view, name='dashboard_event_create'),
    path('events/<int:event_id>/edit/', dashboard_views.event_edit_view, name='dashboard_event_edit'),
    path('events/<int:event_id>/delete/', dashboard_views.event_delete_view, name='dashboard_event_delete'),
    path('events/stats/', dashboard_views.event_stats_view, name='dashboard_event_stats'),

]
