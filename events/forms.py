from django import forms
from .models import Prediction, Match
from django.shortcuts import get_object_or_404


class PredictionForm(forms.ModelForm):
    home_result = forms.IntegerField()
    away_result = forms.IntegerField()

    class Meta:
        model = Prediction
        fields = ['home_result', 'home_result']

    def __init__(self, *args, **kwargs):
        match_id = kwargs.pop('id', None)
        super(PredictionForm, self).__init__(*args, **kwargs)
        match = get_object_or_404(Match, id=match_id)
        self.fields['home_result'].label = 'Resultado %s' % (match.home_team)
        self.fields['away_result'].label = 'Resultado %s' % (match.away_team)
