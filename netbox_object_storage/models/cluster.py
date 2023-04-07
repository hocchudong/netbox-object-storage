from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from taggit.models import Tag
from django.core.exceptions import ValidationError
from utilities.choices import ChoiceSet


class ClusterTypeChoice(ChoiceSet):

    CHOICES = [
        ('device', 'Device'),
        ('vm', 'VM'),
        ('devicevm', 'Device/VM'),

    ]

class Cluster(NetBoxModel):
    name = models.CharField(
        max_length=100,
        null=True
    )

    type = models.CharField(
        choices=ClusterTypeChoice,
        max_length=20,
        null=True,
    )

    devices = models.ManyToManyField(
        to='dcim.Device', 
        related_name='s3cluster_device',
        blank=True,
        default=None
    )

    virtualmachine = models.ManyToManyField(
        to='virtualization.VirtualMachine', 
        related_name='s3cluster_vm',
        blank=True,
        default=None
    )

    description = models.CharField(
        max_length=500,
        blank=True
    )

    comments = models.TextField(
        blank=True
    )

    tags = models.ManyToManyField(
        Tag, 
        related_name='s3_clusters'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(f"{self.name}")

    def get_absolute_url(self):
        return reverse('plugins:netbox_object_storage:cluster', args=[self.pk])

    def clean(self):
        # Check if name is existed, raise Validation Error
        if Cluster.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError('A cluster with this name already exists.')