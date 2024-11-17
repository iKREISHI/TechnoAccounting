from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from apps.users.forms.registration import RegistrationForm


# Create your views here.
class RegistrationView(View):
    template_name = "users/registration.html"
    context = {
        'title': 'Регистрация пользователя',
        'form': RegistrationForm
    }

    def get(self, request):
        context = self.context
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.context
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Уведомление пользователя
            messages.success(
                request,
                "Вы успешно зарегистрировались! "
                "После подтверждения вашей учетной записи администратором вы сможете войти."
            )
            return redirect('homepage')

        context.update({'form': form})
        return render(request, self.template_name, context)
