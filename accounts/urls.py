from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view,       name='login'),
    path('logout/', views.logout_view,     name='logout'),
    path('profile/', views.profile_view,   name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/delete/', views.delete_account_view, name='delete_account'),

    path('password/change/', views.password_change_view, name='password_change'),

]
