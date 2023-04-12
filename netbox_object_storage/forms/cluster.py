from ..models import S3Cluster
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelMultipleChoiceField
from django import forms
from dcim.models import Device
from virtualization.models import VirtualMachine
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from tenancy.models import Contact
from utilities.forms import (
    TagFilterField,
)

class S3ClusterForm(NetBoxModelForm):
    name = forms.CharField(
        label='Name',
    )

    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False
    )

    raw_size = forms.IntegerField(
        required=False,
        label='Raw Size',
    )

    used_size = forms.IntegerField(
        required=False,
        label='Used Size',
    )

    comments = CommentField()

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )


    fieldsets = (
        (
            'General', ('name', 'type','description','tags')
        ),
        (
            'Cluster Size', ('raw_size', 'used_size')
        ),
        (
            'Contact', ('contact',)
        ),
    )
    class Meta:
        model = S3Cluster
        fields = (
            'name', 
            'type', 
            'contact',
            'raw_size',
            'used_size',
            'description',
            'comments', 
            'tags')


class S3ClusterFilterForm(NetBoxModelFilterSetForm):
    model = S3Cluster

    fieldsets = (
        (None, ('q', 'filter_id', 'tag',)),
        ('S3Cluster', (
            'type', 'virtualmachine_id', 'devices_id', 'contact_id'
        ))
    )

    virtualmachine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label='VM'
    )

    contact_id = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label='Contact'
    )

    devices_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label='Device'
    )

    type = forms.CharField(
        required=False
    )

    tag = TagFilterField(model)