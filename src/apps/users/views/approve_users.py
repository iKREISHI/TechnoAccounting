from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator

User = get_user_model()


class ApproveUsersListView(UserPassesTestMixin, ListView):
    model = User
    template_name = "users/approve_users.html"
    context_object_name = "users"
    queryset = User.objects.filter(is_active=False)
    paginate_by = 10  # Пагинация по 10 пользователей

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для доступа к этой странице.")
        return redirect('homepage')

    def get_queryset(self):
        # Вы можете обновить queryset с учетом фильтров, если нужно.
        return User.objects.filter(is_active=False)

    def post(self, request, *args, **kwargs):
        user_ids = request.POST.getlist('user_ids')
        if user_ids:
            users_to_activate = User.objects.filter(id__in=user_ids, is_active=False)
            users_to_activate.update(is_active=True)

            messages.success(request, f"Активировано пользователей: {users_to_activate.count()}.")
        else:
            messages.warning(request, "Не выбрано ни одного пользователя.")

        return redirect('approve_users_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)  # Создание пагинатора
        page_number = self.request.GET.get('page')  # Получаем номер страницы из GET-запроса
        page_obj = paginator.get_page(page_number)  # Получаем страницу с пользователями

        context['users'] = page_obj.object_list  # Перезаписываем пользователей с учетом пагинации
        context['page_obj'] = page_obj  # Добавляем информацию о пагинации для шаблона
        context['paginator'] = paginator  # Пагинатор для использования в шаблоне
        return context
