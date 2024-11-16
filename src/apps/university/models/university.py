from django.db import models


class University(models.Model):
    fullname = models.CharField(
        max_length=255, verbose_name="Название университета",
        blank=True, null=False,
    )
    abbreviation = models.CharField(
        max_length=16, verbose_name='Аббревиатура',
        blank=True, null=False,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=False, null=True,
    )

    def __str__(self):
        return self.abbreviation


class UniversityUnit(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=120, verbose_name='Название подразделения ВУЗа',
        blank=True, null=False,
    )
    description = models.TextField(
        verbose_name='Описание подразделения',
        blank=False, null=True,
    )

    def __str__(self):
        return self.name


class UniversityBuilding(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=120, verbose_name='Корпус ВУЗа',
        blank=True, null=False,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=False, null=True,
    )

    def __str__(self):
        return self.name


class Auditorium(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    university_unit = models.ForeignKey(UniversityUnit, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=20, verbose_name='Имя аудитории',
        blank=True, null=False,
    )
    description = models.TextField(
        verbose_name='Описание аудитории'
    )


