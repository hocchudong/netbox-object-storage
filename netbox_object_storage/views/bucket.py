from netbox.views import generic
from .. import forms, models, tables
from utilities.views import register_model_view
from .. import filtersets


@register_model_view(models.Bucket)
class BucketView(generic.ObjectView):
    queryset = models.Bucket.objects.all()


class BucketListView(generic.ObjectListView):
    queryset = models.Bucket.objects.all()
    table = tables.BucketTable
    filterset = filtersets.BucketFilterSet
    filterset_form = forms.BucketFilterForm


@register_model_view(models.Bucket, 'edit')
class BucketEditView(generic.ObjectEditView):
    queryset = models.Bucket.objects.all()
    form = forms.BucketForm
    template_name = 'netbox_object_storage/bucket_edit.html'


@register_model_view(models.Bucket, 'delete')
class BucketDeleteView(generic.ObjectDeleteView):
    queryset = models.Bucket.objects.all()


class BucketBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Bucket.objects.all()
    table = tables.BucketTable