from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from django.core.exceptions import ValidationError
# from utilities.choices import ChoiceSet


# class ClusterTypeChoice(ChoiceSet):

#     CHOICES = [
#         ('device', 'Device'),
#         ('vm', 'VM'),
#         ('devicevm', 'Device/VM'),

#     ]

class S3Cluster(NetBoxModel):
    name = models.CharField(
        max_length=100,
        null=True
    )

    type = models.CharField(
        blank=True,
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

    contact = models.ForeignKey(
        to='tenancy.Contact',
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        default=None,
        related_name='s3cluster_contact',
    )

    s3device_count = models.IntegerField(
        null=True, 
        blank=True, 
        default=None,
        verbose_name = 'Device Count'
    )

    s3vm_count = models.IntegerField(
        null=True, 
        blank=True,
        default=None,
        verbose_name = 'VM Count'
    )

    raw_size = models.IntegerField(
        null=True, 
        blank=True, 
        default=None,
        verbose_name = 'Raw Size'
    )

    used_size = models.IntegerField(
        null=True, 
        blank=True, 
        default=None,
        verbose_name = 'Used Size'
    )

    description = models.CharField(
        max_length=500,
        blank=True
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(f"{self.name}")

    def get_absolute_url(self):
        return reverse('plugins:netbox_object_storage:s3cluster', args=[self.pk])

    def clean(self):
        # Check if name is existed, raise Validation Error
        if S3Cluster.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError('A cluster with this name already exists.')