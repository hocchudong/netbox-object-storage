from virtualization.models import VirtualMachine
from dcim.models import Device, Rack, Region, Site, SiteGroup
from django import forms
from utilities.forms import ConfirmationForm, BootstrapMixin
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField


### Device ADD
class ClusterAddDevicesForm(BootstrapMixin, forms.Form):
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        null_option='None'
    )
    site_group = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        null_option='None'
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region',
            'group_id': '$site_group',
        }
    )
    rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site'
        }
    )
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        query_params={
            'site_id': '$site',
            'rack_id': '$rack',
        }
    )

    class Meta:
        fields = [
            'region', 'site', 'rack', 'devices',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['devices'].choices = []

### Device Remove

class ClusterRemoveDevicesForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Device.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


# VM ADD
class ClusterAddVMsForm(BootstrapMixin, forms.Form):
    virtualmachine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
    )
    class Meta:
        fields = [
            'cluster', 'virtualmachine'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['virtualmachine'].choices = []


### VM Remove
class ClusterRemoveVMsForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
