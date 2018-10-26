from django import forms
from .models import Prediction, Match, Question
from django.shortcuts import get_object_or_404
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple


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


class TriviaForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(TriviaForm, self).__init__(*args, **kwargs)
        question_list = Question.objects.all()
        for question in question_list:
            if question.multiple:
                self.fields['question-%s' % question.id] = forms.ModelMultipleChoiceField(queryset=question.options, widget=CheckboxSelectMultiple(), label=question.text, required=True)
            else:
                self.fields['question-%s' % question.id] = forms.ModelChoiceField(queryset=question.options, widget=RadioSelect(), label=question.text, required=True, empty_label=None)
