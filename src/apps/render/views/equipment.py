from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.db.models import Q

from apps.accounting.models import Equipment


class EquipmentView(ListView):
    template_name = "render/equipment/main.html"
    model = Equipment
    context_object_name = 'equipment_list'
    paginate_by = 5
    ordering = ['-id']

    def get_queryset(self):
        queryset = Equipment.objects.all()

        # Поиск
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(inventory_number__icontains=search_query)
            )

        # Сортировка
        sort_option = self.request.GET.get('sort', 'name')  # По умолчанию сортируем по имени
        if sort_option in ['name', '-name', 'registration_datetime', '-registration_datetime']:
            queryset = queryset.order_by(sort_option)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')  # Для заполнения поля поиска
        context['sort_option'] = self.request.GET.get('sort', 'name')  # Для отображения активной сортировки
        return context