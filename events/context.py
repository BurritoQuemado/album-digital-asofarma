from django.utils import timezone
from .models import Match, Trivia


def events(request):
    if request.user.is_authenticated:
        predictions = Match.objects.filter(active_until__gte=timezone.now()).exclude(match_prediction__user=request.user)
        trivia = Trivia.objects.filter(user=request.user)
        return {'events': predictions, 'trivia': trivia}
    return {}
