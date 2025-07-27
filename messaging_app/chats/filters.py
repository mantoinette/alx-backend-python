# chats/filters.py

import django_filters
from .models import Message
from django.contrib.auth.models import User

class MessageFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(
        field_name='conversation__participants',
        queryset=User.objects.all(),
        label="Filter by user in conversation"
    )
    start_date = django_filters.DateFilter(
        field_name='timestamp', lookup_expr='gte', label="Start date"
    )
    end_date = django_filters.DateFilter(
        field_name='timestamp', lookup_expr='lte', label="End date"
    )

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']
