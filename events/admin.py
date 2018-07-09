from django.contrib import admin
from .models import Match, Prediction, Question, Option
from django.contrib.admin import SimpleListFilter


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'away_result', 'home_result', )
    fields = ('home_team', 'away_team', 'away_result', 'home_result', 'active_until',)


class CorrectFilter(SimpleListFilter):
    title = 'prediccion correcta'
    parameter_name = 'correct'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('correct', 'Predicción correcta'),
            ('incorrect', 'Predicción incorrecta'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'correct':
            predictions = queryset.all()
            match = predictions.first().match
            return predictions.filter(away_result=match.away_result, home_result=match.home_result)

        if self.value() == 'incorrect':
            predictions = queryset.all()
            match = predictions.first().match
            return queryset.all().exclude(away_result=match.away_result, home_result=match.home_result)


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'match', 'created_at',)
    list_filter = ('match__id', CorrectFilter)

    # def get_queryset(self, request):
    #     qs = super(PredictionAdmin, self).get_queryset(request)
    #     match = Match.objects.all().first()
    #     return qs.filter(away_result=match.away_result, home_result=match.home_result)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at',)
    fields = ['text', 'is_correct']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at',)
    fields = ['text', 'options', 'multiple']
