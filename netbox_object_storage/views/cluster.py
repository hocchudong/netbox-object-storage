from netbox.views import generic
from .. import forms, models, tables
from .. import filtersets
from django.db.models import Count, Sum


class S3ClusterView(generic.ObjectView):
    queryset = models.S3Cluster.objects.all()
    def get_extra_context(self, request, instance):
        pool_table = tables.PoolTable(instance.pool_cluster.all())
        instance_resource = instance.virtualmachine.aggregate(
            vcpus_sum=Sum('vcpus'), 
            memory_sum=Sum('memory'), 
            disk_sum=Sum('disk')
        )
        return {
            'instance_resource': instance_resource,
            'pool_table': pool_table
        }


class S3ClusterListView(generic.ObjectListView):
    queryset = models.S3Cluster.objects.annotate(
        dv_count=Count('devices', distinct=True),
        vm_count=Count('virtualmachine', distinct=True),
    )
    table = tables.S3ClusterTable
    filterset = filtersets.S3ClusterFilterSet
    filterset_form = forms.S3ClusterFilterForm


class S3ClusterEditView(generic.ObjectEditView):
    queryset = models.S3Cluster.objects.all()
    form = forms.S3ClusterForm


class S3ClusterDeleteView(generic.ObjectDeleteView):
    queryset = models.S3Cluster.objects.all()


class S3ClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = models.S3Cluster.objects.all()
    table = tables.S3ClusterTable