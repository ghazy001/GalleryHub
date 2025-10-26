from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # show is_banned in admin list
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_banned', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_banned', 'is_active')
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Status', {'fields': ('is_banned',)}),
    )
