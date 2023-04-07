from ..models import Pool, Cluster, PoolTypeChoices
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms import ConfirmationForm, BootstrapMixin, TagFilterField, MultipleChoiceField
from django import forms


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

class PoolFilterForm(NetBoxModelFilterSetForm):
    model = Pool
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Pool', (
            'type', 'size', 'cluster_id'
        ))
    )

    type = MultipleChoiceField(
        choices=PoolTypeChoices,
        required=False,
    )

    size = forms.IntegerField(
        required=False
    )

    cluster_id = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label='Cluster'
    )

    tag = TagFilterField(model)