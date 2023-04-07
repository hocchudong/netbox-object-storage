from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from ..models import Pool, Cluster
import django_filters


class PoolFilterSet(NetBoxModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster',
        queryset=Cluster.objects.all(),
        label='Cluster (ID)',
    )

    class Meta:
        model = Pool
        fields = (
            'id', 
            'name', 
            'type', 
            'size', 
            'cluster'
        )
        
    def search(self, queryset, name, value):
        query = Q(
            Q(name__icontains=value) |
            Q(type__icontains=value) |
            Q(cluster__name__icontains=value) |
            Q(size__icontains=value)
        )
        return queryset.filter(query)