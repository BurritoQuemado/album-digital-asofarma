from django.contrib import admin
from .models import Match, Prediction


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'away_result', 'home_result', )
    fields = ('home_team', 'away_team', 'away_result', 'home_result', 'active_until',)


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)

    def get_queryset(self, request):
        qs = super(PredictionAdmin, self).get_queryset(request)
        match = Match.objects.all().first()
        return qs.filter(away_result=match.away_result, home_result=match.home_result)
