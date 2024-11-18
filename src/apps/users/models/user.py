from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.university.models import UniversityUnit


class User(AbstractUser):
    patronymic = models.CharField(max_length=100, verbose_name='Отчетсво', blank=True)
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True, blank=True
    )
    phone_number = models.CharField(max_length=17, null=True, verbose_name='Номер телефона')

    university_unit = models.ForeignKey(
        UniversityUnit,
        on_delete=models.PROTECT,
        verbose_name='Подразделение университета',
        null=True,
    )

    def __str__(self):
        last_name = '' if not self.last_name else self.last_name[0].upper() + self.last_name[1:]
        first_name = '' if not self.first_name else self.first_name[0].upper() + self.first_name[1:]
        patronymic = '' if not self.patronymic else self.patronymic[0].upper() + self.patronymic[1:]

        return f'{last_name} {first_name} {patronymic}'.strip()
