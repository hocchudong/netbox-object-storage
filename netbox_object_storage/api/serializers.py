from rest_framework import serializers
from netbox.constants import NESTED_SERIALIZER_PREFIX
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from netbox.api.fields import ContentTypeField
from ..models import S3Cluster, Bucket, Pool
from utilities.api import get_serializer_for_model
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_serializer_method



class NestedBucketSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_object_storage-api:bucket-detail'
    )

    class Meta:
        model = Bucket
        fields = [
            'id', 'url', 'display'
        ]


class BucketSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_object_storage-api:bucket-detail'
    )

    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bucket
        fields = fields = (
            'id', 'url', 'display', 'name', 'capacity', 'credential', 'contact',
            'url', 'access','assigned_object_type', 'assigned_object_id', 'assigned_object', 
            'description', 'comments', 'tags', 'custom_fields', 'created', 'last_updated'
        )

    @swagger_serializer_method(serializer_or_field=serializers.JSONField)
    def get_assigned_object(self, instance):
        if instance.assigned_object is None:
            raise ValidationError('Assigned Storage is None')
        serializer = get_serializer_for_model(instance.assigned_object, prefix=NESTED_SERIALIZER_PREFIX)
        context = {'request': self.context['request']}
        return serializer(instance.assigned_object, context=context).data


class NestedS3ClusterSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_object_storage-api:s3cluster-detail'
    )

    class Meta:
        model = S3Cluster
        fields = ('id', 'url', 'display', 'name', 'type')


class S3ClusterSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_object_storage-api:s3cluster-detail'
    )

    class Meta:
        model = S3Cluster
        fields = (
            'id', 'url', 'display', 'name', 'type', 'contact',
            'raw_size', 'used_size', 'description', 'comments', 
            'tags', 'custom_fields', 'created', 'last_updated',
        )

class NestedPoolSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_object_storage-api:pool-detail'
    )

    class Meta:
        model = Pool
        fields = ('id', 'url', 'display', 'name', 'type', 'size')


class PoolSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_object_storage-api:pool-detail'
    )

    class Meta:
        model = Pool
        fields = (
            'id', 'url', 'display', 'type', 'size', 'contact',
            'description', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )