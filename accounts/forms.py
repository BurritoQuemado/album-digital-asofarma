from django import forms
from registration.forms import RegistrationForm
from .models import User


class RegistrationForm(RegistrationForm):
    email = forms.EmailField(required=True, label='Correo', error_messages={'unique': "Ya existe un usuario con este correo."})
    first_name = forms.CharField(required=True, label='Nombre(s)',)
    last_name = forms.CharField(required=True, label='Apellidos',)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
