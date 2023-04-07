from ..models import Pool
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
# from utilities.forms import ConfirmationForm, BootstrapMixin
# from django import forms
# from dcim.models import Device, DeviceRole, Platform, Rack, Region, Site, SiteGroup
# from ipam.models import IPAddress
# from tenancy.models import Contact
# from virtualization.models import ClusterGroup, Cluster, VirtualMachine


class PoolForm(NetBoxModelForm):
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
                'size', 
                'cluster',
                'description',
                'tags'
            )
        ),
    )
    class Meta:
        model = Pool
        fields = (
            'name', 
            'type', 
            'size',
            'cluster',
            'description',
            'comments', 
            'tags')