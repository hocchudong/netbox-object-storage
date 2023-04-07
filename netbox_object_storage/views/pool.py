from netbox.views import generic
from .. import forms, models, tables

class PoolView(generic.ObjectView):
    queryset = models.Pool.objects.all()


class PoolListView(generic.ObjectListView):
    queryset = models.Pool.objects.all()
    table = tables.PoolTable


class PoolEditView(generic.ObjectEditView):
    queryset = models.Pool.objects.all()
    form = forms.PoolForm


class PoolDeleteView(generic.ObjectDeleteView):
    queryset = models.Pool.objects.all()


class PoolBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Pool.objects.all()
    table = tables.PoolTable