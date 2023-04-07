from ..models import Cluster, ClusterTypeChoice
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from django import forms
from dcim.models import Device
from virtualization.models import VirtualMachine
from utilities.forms import TagFilterField, MultipleChoiceField

from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple


class ClusterForm(NetBoxModelForm):
    name = forms.CharField(
        label='Name',
    )

    comments = CommentField()

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    fieldsets = (
        (
            'General', 
            (
                'name', 
                'type',
                'description',
                'tags'
            )
        ),
    )
    class Meta:
        model = Cluster
        fields = (
            'name', 
            'type', 
            'description',
            'comments', 
            'tags')


class ClusterFilterForm(NetBoxModelFilterSetForm):
    model = Cluster

    fieldsets = (
        (None, ('q', 'filter_id')),
        ('Cluster', (
            'type', 'virtualmachine_id', 'devices_id'
        ))
    )

    virtualmachine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label='VM'
    )

    devices_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label='Device'
    )

    type = MultipleChoiceField(
        choices=ClusterTypeChoice,
        required=False,
    )
    # tag = TagFilterField(model)