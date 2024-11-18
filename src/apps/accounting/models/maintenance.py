from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.accounting.models import Equipment


class Maintenance(models.Model):
    equipment = models.ManyToManyField(
        Equipment,
        verbose_name="Оборудование",
        blank=False,
    )

    service_worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Обслуживающий персонал',
        related_name='maintenances_as_service_worker',
        blank=False,
        null=False,
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь, сообщивший о неисправности',
        related_name='maintenances_as_reporter',
        blank=False,
        null=False,
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Утверждённый',
        related_name='maintenances_as_assigned_by',
        blank=False,
        null=False,
    )

    issue_description = models.TextField(
        blank=True,
        verbose_name='Описание неисправности',
        null=False,
    )

    STATUS_CHOICES = (
        ('pending', 'в ожидании'),
        ('progress', 'в процессе'),
        ('completed', 'завершено'),
    )

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=32,
        default='pending',
        verbose_name='Статус обслуживания',
        blank=False,
        null=False,
    )

    start_time = models.DateTimeField(
        auto_now=True,
        blank=False,
        verbose_name='Время начала обслуживания'
    )

    end_time = models.DateTimeField(
        auto_now=False,
        blank=False,
        verbose_name='Время окончания обслуживания',
    )

    def __str__(self):
        return self.equipment.first().name + ' ' + self.service_worker.__str__()
