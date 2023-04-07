from ..models import Bucket
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
# from utilities.forms import ConfirmationForm, BootstrapMixin
from django import forms
from ..models import Cluster
from ..models import Pool


class BucketForm(NetBoxModelForm):
    TYPE_CHOICES = (
        ('cluster', 'Cluster'),
        ('pool', 'Pool'),
    )

    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
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
    # fieldsets = (
    #     (
    #         'General', 
    #         (
    #             'name', 
    #             'access',
    #             'capacity', 
    #             'credential', 
    #             'url', 
    #             'description',
    #             'tags'
    #         )
    #     ),
    # )
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
            if type(instance.assigned_object) is Cluster:
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