from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from .cluster import Cluster
from .pool import Pool
from django.contrib.contenttypes.models import ContentType
from ..constants import BUCKET_ASSIGNMENT_MODELS
from django.core.exceptions import ValidationError


class BucketAccessChoices(ChoiceSet):

    CHOICES = [
        ('public', 'Public', 'red'),
        ('private', 'Private', 'green')
    ]


class Bucket(NetBoxModel):
    name = models.CharField(
        max_length=100,
        null=True,
        verbose_name = 'Name'
    )

    capacity = models.IntegerField(
        default=0,
        null=True,
        verbose_name = 'Capacity (GB)'
    )

    credential = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name = 'Credential'
    )

    url = models.URLField(
        null=True,
        blank=True,
        verbose_name = 'Url'
    )

    access = models.CharField(
        max_length=20,
        choices=BucketAccessChoices,
        default='private',
        verbose_name = 'Access',
        blank=True
    )

    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=BUCKET_ASSIGNMENT_MODELS,
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        default=None,
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        default=None
    )

    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )

    description = models.CharField(
        max_length=500,
        blank=True
    )

    comments = models.TextField(
        blank=True
    )

    # prerequisite_models = (
    #     'Cluster',
    #     'Pool'
    # )
    class Meta:
        ordering = ('name',)
        verbose_name = 'Bucket'
        constraints = (
            models.UniqueConstraint(
                fields=('assigned_object_type', 'assigned_object_id'),
                name='bucket_assigned_object'
            ),
        )

    def __str__(self):
        if self.pk is not None:
            return f'{self.assigned_object} <> {self.name}'
        return super().__str__()

    def get_absolute_url(self):
        return reverse('plugins:netbox_object_storage:bucket', args=[self.pk])

    def clean(self):
        # Only check is assigned_object is set.  Required otherwise we have an Integrity Error thrown.
        if self.assigned_object:
            obj_id = self.assigned_object.pk
            obj_type = ContentType.objects.get_for_model(self.assigned_object)
            if Bucket.objects.filter(assigned_object_id=obj_id, assigned_object_type=obj_type).\
                    exclude(pk=self.pk).count() > 0:
                raise ValidationError(f'Bucket already assigned ({self.assigned_object})')
        # Check if name is existed, raise Validation Error
        if Bucket.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError('A bucket with this name already exists.')