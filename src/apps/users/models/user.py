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
    )

    def __str__(self):
        return self.last_name + ' ' + self.first_name[0] + ' ' + self.patronymic[0]
