from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from apps.accounting.models import Equipment
from apps.accounting.serializers.equipment import EquipmentSerializer
from apps.api_v0.permissions import IsOwnerOrStaff


class EquipmentModelViewSet(ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except ValidationError as e:
            raise ValidationError(f"Ошибка при создании оборудования: {str(e)}")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)
