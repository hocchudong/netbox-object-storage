from netbox.api.viewsets import NetBoxModelViewSet
from .. import models
from .serializers import BucketSerializer, S3ClusterSerializer, PoolSerializer


class BucketViewSet(NetBoxModelViewSet):
    queryset = models.Bucket.objects.prefetch_related(
       'tags', 'assigned_object'
    )
    serializer_class = BucketSerializer


class PoolViewSet(NetBoxModelViewSet):
    queryset = models.Pool.objects.prefetch_related('tags')
    serializer_class = PoolSerializer


class S3ClusterViewSet(NetBoxModelViewSet):
    queryset = models.S3Cluster.objects.prefetch_related('tags')
    serializer_class = S3ClusterSerializer
    # filterset_class = filtersets.ProjectFilterSet