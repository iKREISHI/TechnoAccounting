from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'university_unit', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'university_unit')
    search_fields = ('username', 'email', 'last_name', 'first_name', 'phone_number')
    ordering = ('last_name', 'first_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'university_unit')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'university_unit', 'is_active', 'is_staff'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
