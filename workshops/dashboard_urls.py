from django.urls import path
from . import dashboard_views

urlpatterns = [
    # materials
    path('materials/', dashboard_views.material_list_view, name='dashboard_material_list'),
    path('materials/create/', dashboard_views.material_create_view, name='dashboard_material_create'),
    path('materials/<int:material_id>/edit/', dashboard_views.material_edit_view, name='dashboard_material_edit'),
    path('materials/<int:material_id>/delete/', dashboard_views.material_delete_view, name='dashboard_material_delete'),
    path('materials/export/xlsx/', dashboard_views.material_export_excel_view, name='dashboard_material_export'),

    # workshops
    path('workshops/', dashboard_views.workshop_list_view, name='dashboard_workshop_list'),
    path('workshops/create/', dashboard_views.workshop_create_view, name='dashboard_workshop_create'),
    path('workshops/<int:workshop_id>/edit/', dashboard_views.workshop_edit_view, name='dashboard_workshop_edit'),
    path('workshops/<int:workshop_id>/delete/', dashboard_views.workshop_delete_view, name='dashboard_workshop_delete'),
    path('workshops/stats/', dashboard_views.workshop_stats_view, name='dashboard_workshop_stats'),

]
