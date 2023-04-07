from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from ..models import Bucket
import django_filters
from utilities.filters import (
    ContentTypeFilter,
)

class BucketFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()

    class Meta:
        model = Bucket
        fields = (
            'id', 
            'name', 
            'capacity', 
            'credential', 
            'url',
            'access',
            'assigned_object_type_id'
        )
        
    def search(self, queryset, name, value):
        query = Q(
            Q(name__icontains=value) |
            Q(capacity__icontains=value) |
            Q(credential__icontains=value) |
            Q(access__icontains=value) |
            Q(url__icontains=value)
        )
        return queryset.filter(query)

    def filter_assigned_object(self, queryset, name, value):
        query = queryset.filter(
            Q(**{'{}__in'.format(name): value})
        )
        return query