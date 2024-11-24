from django.contrib import admin
from .models import Location, Equipment, Maintenance, Notification, Rental
from apps.university.models import UniversityBuilding, Auditorium
from django.contrib.auth import get_user_model
User = get_user_model()


class LocationAdmin(admin.ModelAdmin):
    list_display = ('auditorium', 'description')
    list_filter = ('auditorium', )
    search_fields = ('auditorium__name', )
    ordering = ('auditorium',)
    fieldsets = (
        (None, {'fields': ('auditorium', 'description')}),
    )

    verbose_name = "Расположение"
    verbose_name_plural = "Расположения"
    list_display_links = ('auditorium',)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory_number', 'count', 'status', 'location', 'owner')
    list_filter = ('status', 'location')
    search_fields = ('name', 'inventory_number', 'description')
    ordering = ('name',)

    # Убираем поле 'registration_datetime' из списка редактируемых
    fieldsets = (
        (
        None, {'fields': ('name', 'inventory_number', 'count', 'photo', 'description', 'status', 'location', 'owner')}),
    )
    # или используем exclude
    exclude = ('registration_datetime',)

    # Заголовки для полей на русском
    verbose_name = "Оборудование"
    verbose_name_plural = "Оборудования"
    list_display_links = ('name',)


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('status', 'service_worker', 'reporter', 'assigned_by', 'end_time')
    list_filter = ('status', 'service_worker')
    search_fields = ('issue_description',)
    ordering = ('start_time',)

    fieldsets = (
        (None, {'fields': ('equipment', 'service_worker', 'reporter', 'assigned_by', 'issue_description', 'status', 'end_time')}),
    )

    exclude = ('start_time',)

    verbose_name = "Обслуживание"
    verbose_name_plural = "Обслуживания"
    list_display_links = ('status',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'datetime')
    list_filter = ('user',)
    search_fields = ('message',)
    ordering = ('datetime',)

    # Убираем поле 'datetime' из списка редактируемых
    fieldsets = (
        (None, {'fields': ('user', 'message')}),
    )
    # или используем exclude
    exclude = ('datetime',)

    # Заголовки для полей на русском
    verbose_name = "Уведомление"
    verbose_name_plural = "Уведомления"
    list_display_links = ('message',)


class RentalAdmin(admin.ModelAdmin):
    list_display = ('renter', 'start_time', 'end_time', 'status', 'location')
    list_filter = ('status', 'renter', 'location')
    search_fields = ('renter__username', 'status', 'location__building__name')
    ordering = ('start_time',)
    fieldsets = (
        (None, {'fields': ('equipment', 'renter', 'assign_by', 'start_time', 'end_time', 'actual_return_time', 'status', 'location')}),
    )

    verbose_name = "Аренда"
    verbose_name_plural = "Аренды"
    list_display_links = ('renter',)


# Регистрация моделей с кастомным админом
admin.site.register(Location, LocationAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Rental, RentalAdmin)

# Добавление русских названий для моделей
Location._meta.verbose_name = 'Расположение'
Location._meta.verbose_name_plural = 'Расположения'

Equipment._meta.verbose_name = 'Оборудование'
Equipment._meta.verbose_name_plural = 'Оборудования'

Maintenance._meta.verbose_name = 'Обслуживание'
Maintenance._meta.verbose_name_plural = 'Обслуживания'

Notification._meta.verbose_name = 'Уведомление'
Notification._meta.verbose_name_plural = 'Уведомления'

Rental._meta.verbose_name = 'Аренда'
Rental._meta.verbose_name_plural = 'Аренды'
