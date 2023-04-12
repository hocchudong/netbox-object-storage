from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from ..models import S3Cluster
from dcim.models import Device
from virtualization.models import VirtualMachine
import django_filters
from tenancy.models import Contact


class S3ClusterFilterSet(NetBoxModelFilterSet):
    virtualmachine_id = django_filters.ModelMultipleChoiceFilter(
        field_name='virtualmachine',
        queryset=VirtualMachine.objects.all(),
        label='VM (ID)',
    )

    devices_id = django_filters.ModelMultipleChoiceFilter(
        field_name='devices',
        queryset=Device.objects.all(),
        label='Device (ID)',
    )

    contact_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contact',
        queryset=Contact.objects.all(),
        label='Contact (ID)',
    )

    class Meta:
        model = S3Cluster
        fields = (
            'id', 
            'name', 
            'type', 
            'contact',
            'devices', 
            'virtualmachine'
        )
        
    def search(self, queryset, name, value):
        query = Q(
            Q(name__icontains=value) |
            Q(type__icontains=value) |
            Q(contact__name__icontains=value)

        )
        return queryset.filter(query)