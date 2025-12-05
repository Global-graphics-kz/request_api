import django_filters
from .models import Request

class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        fields = ['user', 'status', 'priority', 'start_date', 'end_date']
        