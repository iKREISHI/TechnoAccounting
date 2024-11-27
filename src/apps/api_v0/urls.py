from rest_framework import routers

from apps.api_v0.views import (
    EquipmentModelViewSet,
    MaintenanceModelViewSet
)

router = routers.DefaultRouter()

router.register(r'equipment', EquipmentModelViewSet, basename='equipment')
router.register(r'maintenance', MaintenanceModelViewSet, basename='maintenance')
# router.register(r'university', UniversityViewSet, basename='university')
# router.register(r'universityunit', UniversityUnitViewSet, basename='universityunit')
# router.register(r'location', LocationViewSet, basename='location')
# router.register(r'universitybuilding', UniversityBuildingViewSet, basename='universitybuilding')
# router.register(r'auditorium', AuditoriumViewSet, basename='auditorium')
urlpatterns = router.urls

