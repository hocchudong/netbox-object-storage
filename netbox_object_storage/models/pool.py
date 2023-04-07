from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from .cluster import Cluster
from django.core.exceptions import ValidationError

class PoolTypeChoices(ChoiceSet):

    CHOICES = [
        ('ssd', 'SSD'),
        ('hdd', 'HDD')
    ]

class Pool(NetBoxModel):
    name = models.CharField(
        max_length=100,
        null=True
    )

    type = models.CharField(
        max_length=15,
        choices=PoolTypeChoices, 
        blank=True
    )

    cluster = models.ForeignKey(
        to='netbox_object_storage.Cluster',
        on_delete=models.SET_NULL,
        related_name='pool_cluster',
        null=True
    )

    size = models.IntegerField(
        default=0,
        verbose_name = 'Size (GB)'
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
        return reverse('plugins:netbox_object_storage:pool', args=[self.pk])

    def clean(self):
        # Check if name is existed, raise Validation Error
        if Pool.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError('A pool with this name already exists.')