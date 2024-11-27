from datetime import timedelta

from rest_framework.exceptions import ValidationError

from apps.accounting.models import Equipment, Maintenance, Location
from apps.university.models import University, UniversityUnit, UniversityBuilding, Auditorium
from apps.users.models import User
from apps.accounting.serializers import MaintenanceSerializer
from django.utils.timezone import now
from django.test import TestCase


class MaintenanceSerializerTest(TestCase):

    def setUp(self):
        """Создаём тестовые данные."""
        # Создаём тестовых пользователей
        self.reporter = User.objects.create_user(
            username="reporter", password="password", email="reporter@example.com"
        )
        self.service_worker = User.objects.create_user(
            username="worker", password="password", email="worker@example.com"
        )
        self.assigned_by = User.objects.create_user(
            username="assigner", password="password", email="assigned@example.com"
        )
        self.owner = User.objects.create_user(
            username="owner", password="password", email="owner@example.com"
        )

        # Создаём объекты для Location
        university = University.objects.create(fullname="Test University", abbreviation="TU")
        unit = UniversityUnit.objects.create(university=university, name="Engineering", abbreviation="ENG")
        building = UniversityBuilding.objects.create(university=university, name="Main Building")
        auditorium = Auditorium.objects.create(
            university=university, university_unit=unit, name="101", building=building
        )
        self.location = Location.objects.create(auditorium=auditorium)

        # Создаём оборудование с указанием location и owner
        self.equipment1 = Equipment.objects.create(
            name="Laptop", inventory_number="INV001", status="available",
            location=self.location, owner=self.owner
        )
        self.equipment2 = Equipment.objects.create(
            name="Printer", inventory_number="INV002", status="available",
            location=self.location, owner=self.owner
        )

    def test_create_maintenance_success(self):
        """Тест на успешное создание заявки на обслуживание."""
        data = {
            "equipment_ids": [self.equipment1.id, self.equipment2.id],
            "service_worker": self.service_worker.username,
            "reporter": self.reporter.username,
            "assigned_by": self.assigned_by.username,
            "issue_description": "Test issue",
            "status": "pending",
            "end_time": now() + timedelta(days=5),
        }

        serializer = MaintenanceSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        maintenance = serializer.save()

        self.assertEqual(maintenance.equipment.count(), 2)
        self.assertEqual(maintenance.service_worker, self.service_worker)
        self.assertEqual(maintenance.reporter, self.reporter)
        self.assertEqual(maintenance.assigned_by, self.assigned_by)
        self.assertEqual(maintenance.status, "pending")
        for equipment in maintenance.equipment.all():
            self.assertEqual(equipment.status, "serviced")

    def test_create_maintenance_without_equipment(self):
        """Проверка валидации при отсутствии оборудования."""
        data = {
            "equipment_ids": [],
            "service_worker": self.service_worker.username,
            "reporter": self.reporter.username,
            "assigned_by": self.assigned_by.username,
            "issue_description": "No equipment test",
            "status": "pending",
            "end_time": now(),
        }

        serializer = MaintenanceSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Equipment is required.", str(context.exception))

    def test_create_maintenance_invalid_status(self):
        """Проверка валидации при некорректном статусе."""
        data = {
            "equipment_ids": [self.equipment1.id],
            "service_worker": self.service_worker.username,
            "reporter": self.reporter.username,
            "assigned_by": self.assigned_by.username,
            "issue_description": "Invalid status test",
            "status": "invalid_status",  # Некорректный статус
            "end_time": now(),
        }

        serializer = MaintenanceSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        print(context.exception)
        self.assertIn("invalid_choice", str(context.exception))

    def test_create_maintenance_past_end_time(self):
        """Проверка валидации на установку времени окончания в прошлом."""
        past_time = now() - timedelta(days=1)
        data = {
            "equipment_ids": [self.equipment1.id],
            "service_worker": self.service_worker.username,
            "reporter": self.reporter.username,
            "assigned_by": self.assigned_by.username,
            "issue_description": "Past end time",
            "status": "pending",
            "end_time": past_time,
        }

        serializer = MaintenanceSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("End time must be in the future", str(context.exception))

    def test_partial_update_status_only(self):
        """Тест на частичное обновление статуса заявки."""
        maintenance = Maintenance.objects.create(
            service_worker=self.service_worker,
            reporter=self.reporter,
            assigned_by=self.assigned_by,
            issue_description="Initial issue",
            status="pending",
            end_time=now(),
        )
        maintenance.equipment.set([self.equipment1])

        updated_data = {"status": "completed"}

        serializer = MaintenanceSerializer(instance=maintenance, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_maintenance = serializer.save()

        self.assertEqual(updated_maintenance.status, "completed")
        self.assertEqual(updated_maintenance.issue_description, "Initial issue")

    def test_update_equipment_list(self):
        """Тест на обновление списка оборудования в заявке."""
        maintenance = Maintenance.objects.create(
            service_worker=self.service_worker,
            reporter=self.reporter,
            assigned_by=self.assigned_by,
            issue_description="Initial issue",
            status="pending",
            end_time=now(),
        )
        maintenance.equipment.set([self.equipment1])

        updated_data = {"equipment_ids": [self.equipment2.id]}

        serializer = MaintenanceSerializer(instance=maintenance, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_maintenance = serializer.save()

        self.assertEqual(updated_maintenance.equipment.count(), 1)
        self.assertIn(self.equipment2, updated_maintenance.equipment.all())
