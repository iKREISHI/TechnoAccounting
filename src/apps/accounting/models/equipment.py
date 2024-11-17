from django.db import models
from apps.university.models import (
    UniversityBuilding, Auditorium,
)
from django.contrib.auth import get_user_model
User = get_user_model()


class Location(models.Model):
    building = models.ForeignKey(
        UniversityBuilding, on_delete=models.CASCADE, verbose_name='Корпус Университета'
    )

    auditorium = models.ForeignKey(
        Auditorium, on_delete=models.CASCADE, verbose_name='Аудитория'
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=False, null=True,
    )


class Equipment(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Оборудование',
        blank=True,
    )

    inventory_number = models.CharField(
        max_length=32, verbose_name='Инвентарный номер',
        blank=True,
    )

    count = models.PositiveIntegerField(
        verbose_name='Количество оборудования',
        blank=True,
        default=1,
    )

    photo = models.ImageField(
        verbose_name='Фото оборудования',
        blank=False,
    )

    description = models.TextField(
        verbose_name='Описание оборудования',
        blank=True,
    )

    STATUS_CHOICES = (
        ('available', 'доступно'),
        ('rented', 'сдан в аренду'),
        ('serviced', 'обслуживается'),
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='available',
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Расположение оборудования'
    )

    registration_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name='Время добавление оборудования',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления',
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец оборудования'
    )
