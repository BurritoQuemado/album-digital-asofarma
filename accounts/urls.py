from django.urls import path, re_path
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        User = get_user_model()
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("No existen usuarios registrados con el correo especificado.")
        return email


app_name = 'accounts'

urlpatterns = [
    # Account Class Views
    path(
        '',
        password_reset,
        {
            'password_reset_form': EmailValidationOnForgotPassword,
            'template_name': 'registration/reset_password_form.html',
            'post_reset_redirect': 'accounts:password_reset_done',
            'email_template_name': 'registration/reset_password_email.html'
        },
        name='password_reset'
    ),
    path(
        'hecho/',
        password_reset_done,
        {
            'template_name': 'registration/reset_password_done.html'
        },
        name='password_reset_done'),
    re_path(
        r'^confirmar/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {
            'template_name': 'registration/reset_password_confirm.html',
            'post_reset_redirect': 'accounts:password_reset_complete'
        },
        name='password_reset_confirm'),
    path(
        'completado/',
        password_reset_complete,
        {
            'template_name': 'registration/reset_password_complete.html'
        },
        name='password_reset_complete'
    )
]
