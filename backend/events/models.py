from django.db import models
from accounts.models import User


class Match(models.Model):

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'

    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    away_result = models.IntegerField(default=0)
    home_result = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    active_until = models.DateTimeField()

    def __str__(self):
        return '%s vs. %s' % (self.home_team, self.away_team)


class Prediction(models.Model):

    class Meta:
        verbose_name = 'Predicción'
        verbose_name_plural = 'Predicciónes'

    match = models.ForeignKey(Match, related_name="match_prediction", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="match_user", on_delete=models.CASCADE)
    away_result = models.IntegerField(verbose_name='Resultado Visitante')
    home_result = models.IntegerField(verbose_name='Resultado Local')
    created_at = models.DateTimeField(auto_now=True)
    submitted = models.BooleanField(default=False)


class Option(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    options = models.ManyToManyField(Option)
    response = models.CharField(max_length=200, null=True, default=None)
    multiple = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Trivia(models.Model):
    user = models.OneToOneField(User, related_name="trivia", on_delete=models.CASCADE)
    options = models.ManyToManyField(Option, related_name='pizzas')
