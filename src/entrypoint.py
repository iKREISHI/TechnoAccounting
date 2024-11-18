import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from apps.university.models import University, UniversityUnit, UniversityBuilding, Auditorium
from apps.users.models import User
from django.contrib.auth.models import Group, Permission

if __name__ == '__main__':
    print('entrypoint')