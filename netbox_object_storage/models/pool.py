from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from django.core.exceptions import ValidationError


class Pool(NetBoxModel):
    name = models.CharField(
        max_length=100,
        null=True
    )

    type = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

    contact = models.ForeignKey(
        to='tenancy.Contact',
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        default=None,
        related_name='s3pool_contact',
    )

    cluster = models.ForeignKey(
        to='netbox_object_storage.S3Cluster',
        on_delete=models.SET_NULL,
        related_name='pool_cluster',
        null=True
    )

    size = models.IntegerField(
        blank=True,
        null=True,
        verbose_name = 'Size (GB)'
    )

    description = models.CharField(
        max_length=500,
        blank=True
    )

    comments = models.TextField(
        blank=True
    )

    # prerequisite_models = (
    #     'netbox_object_storage.S3Cluster',
    # )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(f"{self.name}")

    def get_absolute_url(self):
        return reverse('plugins:netbox_object_storage:pool', args=[self.pk])

    def clean(self):
        # Check if name is existed, raise Validation Error
        if Pool.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError('A pool with this name already exists.')