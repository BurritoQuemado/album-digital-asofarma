from .models import Notification


def departments(request):
    notifications = Notification.objects.filter(receiver=request.user, receiver_read=False)
    return {'alerts': notifications}
