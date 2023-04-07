from ..models import Cluster
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from django import forms


class ClusterForm(NetBoxModelForm):
    TYPE_CHOICES = (
        ('device', 'Device'),
        ('vm', 'VM'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES)
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