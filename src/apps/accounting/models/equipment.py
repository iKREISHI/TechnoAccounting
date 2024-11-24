from django.db import models
from apps.university.models import (
    Location
)
from django.contrib.auth import get_user_model
User = get_user_model()


class Equipment(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Оборудование',
        blank=False, null=False
    )

    inventory_number = models.CharField(
        max_length=32, verbose_name='Инвентарный номер',
        blank=False, null=False
    )

    count = models.PositiveIntegerField(
        verbose_name='Количество оборудования',
        blank=False, null=False,
        default=1,
    )

    photo = models.ImageField(
        verbose_name='Фото оборудования',
        blank=True, null=True,
    )

    description = models.TextField(
        verbose_name='Описание оборудования',
        blank=True, null=True,
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

    def __str__(self):
        return self.name
