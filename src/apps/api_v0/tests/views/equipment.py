from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.users.models import User
from apps.accounting.models import Equipment
from apps.university.models import (
    University, UniversityUnit, UniversityBuilding, Auditorium, Location
)
from django.utils.timezone import now


class EquipmentModelViewSetTests(APITestCase):

    def setUp(self):
        # Создание связанных объектов
        self.university = University.objects.create(
            fullname="Шадринский государственный педагогический университет",
            abbreviation="ШГПУ"
        )
        self.university_unit = UniversityUnit.objects.create(
            university=self.university,
            name="Технопарк",
            abbreviation="ТП",
        )
        self.building = UniversityBuilding.objects.create(
            university=self.university,
            name="Главный корпус",
            address="ул. Советская, д. 1"
        )
        self.auditorium = Auditorium.objects.create(
            university=self.university,
            university_unit=self.university_unit,
            name="Аудитория 101",
            building=self.building,
        )
        self.location = Location.objects.create(
            auditorium=self.auditorium,
            description="Место хранения оборудования"
        )

        # Создание пользователей
        self.staff_user = User.objects.create_user(
            username='staff', password='password', email='staff@<EMAIL>',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user', password='password', email='regular@<EMAIL>',
        )

        # Создание оборудования
        self.equipment = Equipment.objects.create(
            name="Ноутбук Lenovo",
            inventory_number="INV12345",
            count=5,
            status="available",
            location=self.location,
            owner=self.regular_user
        )

        self.client = APIClient()

    def test_list_equipment_as_authenticated_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/api/v0/equipment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Ноутбук Lenovo")

    def test_list_equipment_as_staff_user_with_all_param(self):
        self.client.login(username='staff', password='password')
        response = self.client.get('/api/v0/equipment/?all=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_equipment_as_authenticated_user(self):
        self.client.login(username='user', password='password')
        data = {
            'name': 'Принтер HP',
            'inventory_number': 'INV67890',
            'count': 2,
            'status': 'available',
            'location': self.location.id,
        }
        response = self.client.post('/api/v0/equipment/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), 2)
        new_equipment = Equipment.objects.get(inventory_number='INV67890')
        self.assertEqual(new_equipment.owner, self.regular_user)

    def test_create_equipment_as_unauthenticated_user(self):
        data = {
            'name': 'Принтер HP',
            'inventory_number': 'INV67890',
            'count': 2,
            'status': 'available',
            'location': self.location.id,
        }
        response = self.client.post('/api/v0/equipment/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_equipment_as_owner(self):
        self.client.login(username='user', password='password')
        data = {
            'name': 'Ноутбук Lenovo (Обновленный)',
            'inventory_number': 'INV12345',
            'count': 3,
            'location': self.location.id,
        }
        response = self.client.put(f'/api/v0/equipment/{self.equipment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.equipment.refresh_from_db()
        self.assertEqual(self.equipment.name, 'Ноутбук Lenovo (Обновленный)')
        self.assertEqual(self.equipment.count, 3)

    def test_update_equipment_by_staff_as_non_owner(self):
        self.client.login(username='staff', password='password')
        data = {
            'name': 'Ноутбук Lenovo (Обновленный)',
        }
        response = self.client.patch(f'/api/v0/equipment/{self.equipment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_equipment_by_regular_as_non_owner(self):
        equipment = Equipment.objects.create(
            name="Ноутбук",
            inventory_number="INV12345-1",
            count=5,
            status="available",
            location=self.location,
            owner=self.staff_user
        )
        self.client.login(username='user', password='password')
        data = {
            'name': 'Ноутбук (Обновленный)',
        }
        response = self.client.patch(f'/api/v0/equipment/{equipment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_equipment_as_owner(self):
        self.client.login(username='user', password='password')
        response = self.client.delete(f'/api/v0/equipment/{self.equipment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Equipment.objects.count(), 0)

    def test_retrieve_equipment_as_authenticated_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get(f'/api/v0/equipment/{self.equipment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Ноутбук Lenovo')

    def test_permission_denied_for_all_param_as_regular_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/api/v0/equipment/?all=true')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
