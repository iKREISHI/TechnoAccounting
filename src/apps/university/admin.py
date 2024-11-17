from django.contrib import admin
from .models import University, UniversityUnit, UniversityBuilding, Auditorium

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'abbreviation', 'description')
    list_filter = ('fullname',)
    search_fields = ('fullname', 'abbreviation')
    ordering = ('fullname',)
    fieldsets = (
        (None, {'fields': ('fullname', 'abbreviation', 'description')}),
    )

    # Заголовки для полей на русском
    list_display_links = ('fullname',)


class UniversityUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'description')
    list_filter = ('university',)
    search_fields = ('name', 'university__fullname')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'university', 'description')}),
    )

    # Заголовки для полей на русском
    list_display_links = ('name',)


class UniversityBuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'description')
    list_filter = ('university',)
    search_fields = ('name', 'university__fullname')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'university', 'description')}),
    )

    # Заголовки для полей на русском
    list_display_links = ('name',)


class AuditoriumAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'university_unit', 'description')
    list_filter = ('university', 'university_unit')
    search_fields = ('name', 'university__fullname', 'university_unit__name')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'university', 'university_unit', 'description')}),
    )

    # Заголовки для полей на русском
    list_display_links = ('name',)


# Применение verbose_name и verbose_name_plural для моделей
Auditorium._meta.verbose_name = 'Аудитория'
Auditorium._meta.verbose_name_plural = 'Аудитории'

University._meta.verbose_name = 'Университет'
University._meta.verbose_name_plural = 'Университеты'

UniversityUnit._meta.verbose_name = 'Подразделение университета'
UniversityUnit._meta.verbose_name_plural = 'Подразделения университета'

UniversityBuilding._meta.verbose_name = 'Корпус университета'
UniversityBuilding._meta.verbose_name_plural = 'Корпуса университета'


# Регистрация моделей с кастомным админом
admin.site.register(University, UniversityAdmin)
admin.site.register(UniversityUnit, UniversityUnitAdmin)
admin.site.register(UniversityBuilding, UniversityBuildingAdmin)
admin.site.register(Auditorium, AuditoriumAdmin)

