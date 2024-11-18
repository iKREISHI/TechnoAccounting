from django.db import models
from apps.accounting.models import (
    Equipment, Location
)
from django.contrib.auth import get_user_model
User = get_user_model()


class Rental(models.Model):
    equipment = models.ManyToManyField(
        Equipment,
        verbose_name='Оборудование',
        blank=False,
    )

    renter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Арендатор',
        related_name='rentals_as_renter',
        blank=False,
        null=False,
    )

    assign_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Утверждённый',
        related_name='rentals_as_assign_by',
        blank=False,
        null=False,
    )

    start_time = models.DateTimeField(
        auto_now=False,
        blank=False,
        null=False,
        verbose_name='Время начала аренды',
    )

    end_time = models.DateTimeField(
        auto_now=False,
        blank=False,
        null=False,
        verbose_name='Время окончания аренды',
    )

    actual_return_time = models.DateTimeField(
        auto_now=False,
        blank=False,
        null=False,
        verbose_name='Реальное время возврата оборудования',
    )

    STATUS_CHOICES = (
        ('active', 'активна'),
        ('completed', 'завершена'),
        ('expired', 'просрочена'),
    )

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=32,
        default='active',
        verbose_name='Статус аренды',
        blank=False,
        null=False,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Расположение оборудования на время аренды',
    )
