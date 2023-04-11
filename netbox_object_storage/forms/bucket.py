from ..models import Bucket, S3Cluster, Pool, BucketAccessChoices
from django import forms
from extras.models import Tag
from django.utils.translation import gettext as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from django.contrib.contenttypes.models import ContentType
from utilities.forms import (
    ContentTypeMultipleChoiceField,
    MultipleChoiceField, TagFilterField,
)
from ..constants import BUCKET_ASSIGNMENT_MODELS
from tenancy.models import Contact


class BucketForm(NetBoxModelForm):
    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False
    )

    cluster = DynamicModelChoiceField(
        queryset=S3Cluster.objects.all(),
        required=False,
        query_params={}
    )

    pool = DynamicModelChoiceField(
        queryset=Pool.objects.all(),
        required=False,
        query_params={}
    )

    comments = CommentField()

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Bucket
        fields = (
            'name', 'capacity', 'credential', 'url', 
            'access', 'description', 'comments', 'tags'
            )
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()

        if instance:
            if type(instance.assigned_object) is S3Cluster:
                initial['cluster'] = instance.assigned_object
            elif type(instance.assigned_object) is Pool:
                initial['pool'] = instance.assigned_object
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        cluster = self.cleaned_data.get('cluster')
        pool = self.cleaned_data.get('pool')

        if not (cluster or pool):
            raise ValidationError('A bucket must specify an cluster or pool.')
        if len([x for x in (cluster, pool) if x]) > 1:
            raise ValidationError('A bucket can only have one terminating object (an cluster or pool).')

        self.instance.assigned_object = cluster or pool


class BucketFilterForm(NetBoxModelFilterSetForm):
    model = Bucket
    fieldsets = (
        (None, ('q', 'filter_id', 'tag',)),
        ('Bucket', ('capacity', 'credential', 'url', 'access', 'contact_id')),
        ('Assigned Storage', ('assigned_object_type_id',)),
    )

    access = MultipleChoiceField(
        choices=BucketAccessChoices,
        required=False,
    )

    contact_id = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False,
        label='Contact'
    )

    assigned_object_type_id = ContentTypeMultipleChoiceField(
        queryset=ContentType.objects.filter(BUCKET_ASSIGNMENT_MODELS),
        required=False,
        label=_('Storage Backend Type'),
        limit_choices_to=BUCKET_ASSIGNMENT_MODELS
    )

    capacity = forms.IntegerField(
        required=False
    )

    url = forms.URLField(
        required=False
    )

    credential = forms.CharField(
        required=False
    )

    tag = TagFilterField(model)
