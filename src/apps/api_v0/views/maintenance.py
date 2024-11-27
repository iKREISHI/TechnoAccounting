from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from apps.accounting.models import Maintenance
from apps.accounting.serializers import MaintenanceSerializer
from django.utils.timezone import now


class MaintenanceModelViewSet(viewsets.ModelViewSet):
    """ViewSet для управления заявками на обслуживание."""
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def get_permissions(self):
        """Определение разрешений в зависимости от действия."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Переопределение метода создания записи."""
        try:
            serializer.save(
                reporter=self.request.user,
                start_time=now(),
            )
        except ValidationError as e:
            raise ValidationError(f"Ошибка при создании заявки: {str(e)}")

    def get_queryset(self):
        """Переопределение запроса для фильтрации по пользователю."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return queryset  # Для персонала возвращаем все заявки

        # Для обычных пользователей возвращаем только их заявки
        return queryset.filter(reporter=user)

    def update(self, request, *args, **kwargs):
        """Переопределение метода обновления для проверки прав."""
        instance = self.get_object()
        if request.user != instance.assigned_by and not request.user.is_staff:
            return Response(
                {"detail": "Вы не можете редактировать эту заявку."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Переопределение метода удаления с проверкой прав."""
        instance = self.get_object()
        if request.user != instance.assigned_by and not request.user.is_staff:
            return Response(
                {"detail": "Вы не можете удалить эту заявку."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
