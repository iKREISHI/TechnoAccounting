from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


User = get_user_model()


class InactiveUsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/inactive_users_list.html"  # Шаблон для вывода
    context_object_name = "inactive_users"
    login_url = reverse_lazy('login')  # URL для перенаправления неавторизованных пользователей

    def get_queryset(self):
        return User.objects.filter(is_active=False)
