from .models import Features


def get_max_value(project):
    try:
        return max(sorted(list(Features.objects.filter(project=project).values_list('priority', flat=True))))
    except ValueError:
        return None
