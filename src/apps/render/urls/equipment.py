from django.urls import path
from apps.render.views.equipment import EquipmentView

urlpatterns = [
    path('', EquipmentView.as_view(), name='equipment'),
]