from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Code


class EmailSaveForm(forms.ModelForm):
    code = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Code
        fields = ['code']

    def clean(self):
        cleaned_data = super().clean()
        code_cleaned = cleaned_data.get('code')
        try:
            Code.objects.get(code=code_cleaned)
        except ObjectDoesNotExist:
            raise forms.ValidationError("No existe el código")
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
