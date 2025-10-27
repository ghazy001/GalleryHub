from django.urls import path
from . import dashboard_views

urlpatterns = [
    # categories
    path('categories/', dashboard_views.category_list_view, name='dashboard_category_list'),
    path('categories/create/', dashboard_views.category_create_view, name='dashboard_category_create'),
    path('categories/<int:category_id>/edit/', dashboard_views.category_edit_view, name='dashboard_category_edit'),
    path('categories/<int:category_id>/delete/', dashboard_views.category_delete_view, name='dashboard_category_delete'),
    path('categories/export/xlsx/', dashboard_views.category_export_excel_view, name='dashboard_category_export'),

    # articles
    path('articles/', dashboard_views.article_list_view, name='dashboard_article_list'),
    path('articles/create/', dashboard_views.article_create_view, name='dashboard_article_create'),
    path('articles/<int:article_id>/edit/', dashboard_views.article_edit_view, name='dashboard_article_edit'),
    path('articles/<int:article_id>/delete/', dashboard_views.article_delete_view, name='dashboard_article_delete'),
    path('articles/stats/', dashboard_views.article_stats_view, name='dashboard_article_stats'),

]
