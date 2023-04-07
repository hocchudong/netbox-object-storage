from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import F
from .. import models
from .serializers import BucketSerializer, ClusterSerializer, PoolSerializer
from django.db.models import Count, Subquery, OuterRef


class BucketViewSet(NetBoxModelViewSet):
    queryset = models.Bucket.objects.prefetch_related(
        'tags', 'assigned_object'
    )
    serializer_class = BucketSerializer


class PoolViewSet(NetBoxModelViewSet):
    queryset = models.Pool.objects.prefetch_related('tags')
    serializer_class = PoolSerializer


class ClusterViewSet(NetBoxModelViewSet):
    queryset = models.Cluster.objects.prefetch_related('tags')
    serializer_class = ClusterSerializer
    # filterset_class = filtersets.ProjectFilterSet