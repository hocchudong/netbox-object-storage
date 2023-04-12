from ..models import Pool, S3Cluster
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms import TagFilterField
from django import forms
from tenancy.models import Contact


class PoolForm(NetBoxModelForm):
    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False
    )

    comments = CommentField()

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    fieldsets = (
        (
            'General', ('name', 'type', 'size', 'description', 'tags')
        ),
        (
            'Contact', ('contact',)
        ),
        (
            'S3 Cluster', ('cluster',)
        ),
    )
    class Meta:
        model = Pool
        fields = (
            'name', 
            'type', 
            'size',
            'contact',
            'cluster',
            'description',
            'comments', 
            'tags')

class PoolFilterForm(NetBoxModelFilterSetForm):
    model = Pool
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Pool', (
            'type', 'size', 'cluster_id', 'contact_id'
        ))
    )

    type = forms.CharField(
        required=False,
    )

    contact_id = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label='Contact'
    )

    size = forms.IntegerField(
        required=False
    )

    cluster_id = DynamicModelChoiceField(
        queryset=S3Cluster.objects.all(),
        required=False,
        label='S3Cluster'
    )

    tag = TagFilterField(model)