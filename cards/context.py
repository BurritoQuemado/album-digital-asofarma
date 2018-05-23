from .models import Department


def departments(request):
    departments = Department.objects.all()
    return {'departments': departments}
