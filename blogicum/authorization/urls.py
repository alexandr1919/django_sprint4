from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy

from . import views

app_name = 'authorization'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/password_change/',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy('authorization:password_change_done')
        ),
        name='password_change',
    ),
    path(
        'auth/password_reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('authorization:password_reset_done')
        ),
        name='password_reset',
    ),
    path(
        'auth/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('authorization:password_reset_complete')
        ),
        name='password_reset_confirm',
    ),
    path(
        'auth/registration/',
        views.UserCreateView.as_view(),
        name='registration',
    ),
]
