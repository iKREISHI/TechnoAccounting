from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounting.models import Equipment
from apps.accounting.serializers.equipment import EquipmentSerializer, EquipmentViewOrListSerializer, \
    EquipmentUpdateSerializer
from apps.api_v0.permissions import IsOwnerOrStaff
from django.utils.timezone import now


class EquipmentModelViewSet(ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        try:
            serializer.save(
                owner=self.request.user,
                registration_datetime=now(),
            )
        except ValidationError as e:
            raise ValidationError(f"Ошибка при создании оборудования: {str(e)}")

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_authenticated:
            raise AuthenticationFailed("Вы должны быть авторизованы, чтобы получить доступ к данным.")

        # Проверяем параметр all в GET-запросе
        all_param = self.request.query_params.get('all', '').lower()
        if all_param == 'true':
            if self.request.user.is_staff:
                return queryset  # Возвращаем все записи для staff
            else:
                self.permission_denied(
                    self.request, message="У вас нет прав на просмотр всех записей."
                )
        # Для остальных возвращаем записи, связанные с текущим пользователем
        return queryset

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return EquipmentUpdateSerializer
        elif self.action in ['retrieve', 'list']:
            return EquipmentViewOrListSerializer
        return EquipmentSerializer

    def check_object_permissions(self, request, obj):
        """
        Проверяем, является ли пользователь владельцем объекта или имеет специальные права.
        """
        super().check_object_permissions(request, obj)

        # Если пользователь не является владельцем объекта и не является staff
        if obj.owner != request.user and not request.user.is_staff:
            raise PermissionDenied("У вас нет прав на доступ к этому оборудованию.")

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)  # Проверка прав на объект
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)  # Проверка прав на объект
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)  # Проверка прав на объект
        return super().destroy(request, *args, **kwargs)
