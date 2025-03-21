from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.university.models import UniversityUnit


class User(AbstractUser):
    patronymic = models.CharField(max_length=100, verbose_name='Отчетсво', blank=False, null=False)
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True, blank=True
    )
    phone_number = models.CharField(
        max_length=17, null=False, blank=False,
        verbose_name='Номер телефона'
    )

    university_unit = models.ForeignKey(
        UniversityUnit,
        on_delete=models.PROTECT,
        verbose_name='Подразделение университета',
        null=True, blank=True,
    )

    def __str__(self):
        last_name = '' if not self.last_name else self.last_name
        first_name = '' if not self.first_name else self.first_name[0].upper()
        patronymic = '' if not self.patronymic else self.patronymic[0].upper()

        return f'{last_name} {first_name} {patronymic}'.strip()
