from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from ..models import Pool, S3Cluster
import django_filters
from tenancy.models import Contact


class PoolFilterSet(NetBoxModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster',
        queryset=S3Cluster.objects.all(),
        label='S3Cluster (ID)',
    )

    contact_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contact',
        queryset=Contact.objects.all(),
        label='Contact (ID)',
    )
    class Meta:
        model = Pool
        fields = (
            'id', 
            'name', 
            'type', 
            'contact',
            'size', 
            'cluster'
        )
        
    def search(self, queryset, name, value):
        query = Q(
            Q(name__icontains=value) |
            Q(type__icontains=value) |
            Q(cluster__name__icontains=value) |
            Q(contact__name__icontains=value) |
            Q(size__icontains=value)
        )
        return queryset.filter(query)