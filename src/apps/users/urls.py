from django.urls import path

from apps.users.views.activate_users import InactiveUsersListView
from apps.users.views.approve_users import ApproveUsersListView
from apps.users.views.registration import RegistrationView
from django.contrib.auth import views

urlpatterns = [
    path(
        'registration/', RegistrationView.as_view(), name='registration'
    ),
    path(
        "login/", views.LoginView.as_view(
            template_name="users/login.html",
        ), name="login"
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name='users/change_password.html',
            success_url='/users/password_changed/'
        ),
        name="password_change"
    ),
    path(
        "password_changed/",
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_changed.html',
        ),
        name="password_changed",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path('inactive-users/', InactiveUsersListView.as_view(), name='inactive_users_list'),
    path('approve-users/', ApproveUsersListView.as_view(), name='approve_users_list'),

]
