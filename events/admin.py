from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'away_result', 'home_result', )
    fields = ('home_team', 'away_team', 'away_result', 'home_result', 'active_until',)
