from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from ..models import Cluster
from dcim.models import Device
from virtualization.models import VirtualMachine
import django_filters


class ClusterFilterSet(NetBoxModelFilterSet):
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
    tag_id = django_filters.ModelMultipleChoiceFilter(
        field_name='tags',
        queryset=Tag.objects.all(),
        label=_('Tag'),
    )
    class Meta:
        model = Cluster
        fields = (
            'id', 
            'name', 
            'type', 
            'devices', 
            'virtualmachine'
        )
        
    def search(self, queryset, name, value):
        query = Q(
            Q(name__icontains=value) |
            Q(type__icontains=value)
        )
        return queryset.filter(query)