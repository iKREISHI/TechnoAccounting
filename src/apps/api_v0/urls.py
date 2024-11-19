from rest_framework import routers

from apps.api_v0.views.auditorium_view import AuditoriumViewSet
from apps.api_v0.views.equipment_view import EquipmentViewSet
from apps.api_v0.views.location_view import LocationViewSet
from apps.api_v0.views.university_unit_view import UniversityUnitViewSet
from apps.api_v0.views.university_view import UniversityViewSet
from apps.api_v0.views.universitybuilding_view import UniversityBuildingViewSet

router = routers.DefaultRouter()

router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'university', UniversityViewSet, basename='university')
router.register(r'universityunit', UniversityUnitViewSet, basename='universityunit')
router.register(r'location', LocationViewSet, basename='location')
router.register(r'universitybuilding', UniversityBuildingViewSet, basename='universitybuilding')
router.register(r'auditorium', AuditoriumViewSet, basename='auditorium')
urlpatterns = router.urls

