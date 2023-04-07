from netbox.views import generic
from .. import forms, models, tables
from .. import filtersets


class ClusterView(generic.ObjectView):
    queryset = models.Cluster.objects.all()


class ClusterListView(generic.ObjectListView):
    queryset = models.Cluster.objects.all()
    table = tables.ClusterTable
    filterset = filtersets.ClusterFilterSet
    filterset_form = forms.ClusterFilterForm

class ClusterEditView(generic.ObjectEditView):
    queryset = models.Cluster.objects.all()
    form = forms.ClusterForm


class ClusterDeleteView(generic.ObjectDeleteView):
    queryset = models.Cluster.objects.all()


class ClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Cluster.objects.all()
    table = tables.ClusterTable