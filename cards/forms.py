from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Code
from accounts.models import User


class EmailSaveForm(forms.ModelForm):
    code = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Code
        fields = ['code']

    def clean(self):
        cleaned_data = super().clean()
        code_cleaned = cleaned_data.get('code')
        try:
            Code.objects.get(code=code_cleaned, fk_user=None)
        except ObjectDoesNotExist:
            raise forms.ValidationError("No existe el código o ya fue redimido.")
        return cleaned_data


class AddCodeForm(forms.Form):
    code = forms.CharField(label='Ingresa código para agregar a tu álbum', max_length=8)

    def clean(self):
        cleaned_data = super().clean()
        code_cleaned = cleaned_data.get('code')
        try:
            Code.objects.get(code=code_cleaned)
        except ObjectDoesNotExist:
            raise forms.ValidationError("No existe el código")
        return cleaned_data


class NotificationForm(forms.Form):
    pass


class SendCodeForm(forms.ModelForm):
    code = forms.CharField(widget=forms.HiddenInput())
    user = forms.ModelChoiceField(required=True, queryset=User.objects.all(), label="Selecciona el usuario al cúal le enviarás esta tarjeta")

    class Meta:
        model = Code
        fields = ['code']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super(SendCodeForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False,
        ).exclude(id=user.id).order_by('first_name')

    def clean(self):
        cleaned_data = super().clean()
        code_cleaned = cleaned_data.get('code')
        try:
            Code.objects.get(code=code_cleaned)
        except ObjectDoesNotExist:
            raise forms.ValidationError("No existe el código")
        return cleaned_data
