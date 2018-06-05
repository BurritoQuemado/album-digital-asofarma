from .models import Notification


def departments(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver=request.user, receiver_read=False)
        return {'alerts': notifications}
