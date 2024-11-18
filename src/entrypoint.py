import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from apps.university.models import University, UniversityUnit, UniversityBuilding, Auditorium
from apps.users.models import User
from django.contrib.auth.models import Group, Permission


def create_university():
    fullname = 'Шадринский Государственный Педагогический Университет'
    abbreviation = 'ШГПУ'

    if not University.objects.filter(abbreviation=abbreviation, fullname=fullname).exists():
        university = University.objects.create(abbreviation=abbreviation, fullname=fullname)
        print(f'Unversity created successfully: {university}')
    else:
        print(f'University already exists!')


def create_university_building():
    buildings = [
        {'name': 'Главный корпус', 'address': '641870, Курганская область, г. Шадринск, ул. К.Либкнехта, 3'},
        {'name': 'Корпус №2', 'address': '641870, Курганская область, г. Шадринск, ул. Октябрьская, 98'},
        {'name': 'Корпус №3', 'address': '641870, Курганская область, г. Шадринск, ул. Кондюрина, 28'},
        {'name': 'Корпус №4', 'address': '641870, Курганская область, г. Шадринск, ул. Архангельского, 58'},
    ]
    university = University.objects.filter(abbreviation='ШГПУ',
                                           fullname='Шадринский Государственный Педагогический Университет').first()
    if not university:
        print("University does not exist. Please create it first.")
        return

    for building in buildings:
        if not UniversityBuilding.objects.filter(university=university, name=building['name']).exists():
            UniversityBuilding.objects.create(university=university, name=building['name'], address=building['address'])
            print(f'Building created successfully: {building["name"]}')
        else:
            print(f'Building {building["name"]} already exists!')


def create_university_unit():
    # Получаем объект университета
    university = University.objects.filter(abbreviation='ШГПУ', fullname='Шадринский Государственный Педагогический Университет').first()

    # Проверяем, существует ли университет
    if not university:
        print("University does not exist. Please create it first.")
        return

    name = 'Технопарк УПК'

    if not UniversityUnit.objects.filter(name=name, university=university).exists():
        university_unit = UniversityUnit.objects.create(name=name, university=university)
        print(f'University unit created successfully: {university_unit}')
    else:
        print(f'University unit already exists!')

    units = [
        {'name': "Гуманитарный институт", 'abbreviation': "ГумФак"},
        {'name': 'Институт психологии и педагогики', 'abbreviation': 'ИПиП'},
        {'name': 'Институт информационных технологий, точных и естественных наук', 'abbreviation': 'ИИТТиЕН'},
        {'name': 'Факультет физической культуры', 'abbreviation': 'ФизФак'},
        {'name': 'Университетский колледж', 'abbreviation': 'УК'}
    ]
    for unit in units:
        if not UniversityUnit.objects.filter(name=unit['name']).exists():
            UniversityUnit.objects.create(name=unit['name'], university=university, abbreviation=unit['abbreviation'])
            print(f'University unit created successfully: {unit["name"]}')
        else:
            print(f'University unit: {unit["name"]} already exists!')


def create_superuser():
    username = 'admin'
    email = 'admin@mail.ru'
    password = 'admin'

    if not User.objects.filter(username=username, email=email).exists():
        # Получаем подразделение
        university_unit = UniversityUnit.objects.filter(name='Технопарк УПК').first()

        if not university_unit:
            print("University unit 'Технопарк УПК' does not exist. Please create it first.")
            return

        # Создаем суперпользователя
        user = User.objects.create_superuser(username, email, password)

        user.last_name = 'Admin'
        user.first_name = 'Admin'
        user.patronymic = 'Admin'
        user.university_unit = university_unit  # Здесь передается объект, а не QuerySet

        user.save()
        print(f'Superuser: {username} created')
    else:
        print(f'Superuser: {username} already exists')


def create_technopark_auditorium():
    university = University.objects.filter(abbreviation='ШГПУ',
                                           fullname='Шадринский Государственный Педагогический Университет').first()
    if not university:
        print("University does not exist. Please create it first.")
        return

    university_unit = UniversityUnit.objects.filter(name='Технопарк УПК', university=university).first()
    if not university_unit:
        print("University does not exist. Please create it first.")
        return

    university_building = UniversityBuilding.objects.filter(university=university, name='Главный корпус').first()
    if not university_building:
        print("University does not exist. Please create it first.")
        return

    auditoriums = [
        {
            'university': university, 'university_unit': university_unit,
            'name': '231А - Темнуха', 'building': university_building,
        },
        {
            'university': university, 'university_unit': university_unit,
            'name': '232А', 'building': university_building,
        },
        {
            'university': university, 'university_unit': university_unit,
            'name': '232А - Темнуха', 'building': university_building,
        },
        {
            'university': university, 'university_unit': university_unit,
            'name': '233А', 'building': university_building,
        },
        {
            'university': university, 'university_unit': university_unit,
            'name': '234А', 'building': university_building,
        },
        {
            'university': university, 'university_unit': university_unit,
            'name': '235А', 'building': university_building,
        },
    ]
    for auditorium in auditoriums:
        if not Auditorium.objects.filter(name=auditorium['name']).exists():
            Auditorium.objects.create(**auditorium)
            print(f'Auditorium created successfully: {auditorium["name"]}')
        else:
            print(f'Auditorium already exists!')


if __name__ == '__main__':
    print('entrypoint')
    create_university()
    create_university_unit()
    create_superuser()
    create_university_building()
    create_technopark_auditorium()
