"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.conf.urls import include
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from registration.backends.default.views import RegistrationView
from accounts.forms import RegistrationForm


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        User = get_user_model()
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("No existen usuarios registrados con el correo especificado.")
        return email


urlpatterns = [
    path('', TemplateView.as_view(template_name='views/home.html'), name='home'),
    path(
        'cuenta/password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=EmailValidationOnForgotPassword,
            email_template_name='registration/password_reset_email.html'
        ),
        name='password_reset'
    ),
    path('cuenta/register/', RegistrationView.as_view(
            form_class=RegistrationForm
        ), name='registration_register'),
    path('cuenta/', include('registration.backends.default.urls')),
    path('cuenta/', include('django.contrib.auth.urls')),
    path('dinamicas/', include('events.urls')),
    path('admin/', admin.site.urls),
    path('admin/django-ses/', include('django_ses.urls')),
    path('album/', include('cards.urls')),
]
