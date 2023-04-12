from netbox.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from ..models import S3Cluster
from .. import forms
from django.db import transaction
from dcim.models import Device
from dcim.tables import DeviceTable
from dcim.filtersets import DeviceFilterSet
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.views import ViewTab, register_model_view
from django.contrib import messages


@register_model_view(S3Cluster, 'devices')
class S3ClusterDevicesView(generic.ObjectChildrenView):
    queryset = S3Cluster.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    template_name = 'cluster_assignment/device.html'
    tab = ViewTab(
        label=_('Devices'),
        badge=lambda obj: obj.devices.count() if obj.devices else 0,
        weight=600
    )

     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        device_list = parent.devices.all()
        return Device.objects.restrict(request.user, 'view').filter(
            pk__in=[device.pk for device in device_list]
        )


@register_model_view(S3Cluster, 'add_devices', path='devices/add')
class S3ClusterAddDevicesView(generic.ObjectEditView):
    queryset = S3Cluster.objects.all()
    form = forms.ClusterAddDevicesForm
    template_name = 'cluster_assignment/cluster_add_devices.html'

    def get(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        cluster = get_object_or_404(queryset)
        form = self.form(initial=request.GET)

        return render(request, self.template_name, {
            'cluster': cluster,
            'form': form,
            'return_url': reverse('plugins:netbox_object_storage:s3cluster', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        cluster = get_object_or_404(queryset)
        form = self.form(request.POST)

        if form.is_valid():

            device_pks = form.cleaned_data['devices']
            with transaction.atomic():

                # Assign the selected Devices to the S3Cluster
                for device in Device.objects.filter(pk__in=device_pks):
                    if device in cluster.devices.all():
                        continue
                    else:
                        cluster.devices.add(device)
                        cluster.save()

            messages.success(request, "Added {} devices to cluster {}".format(
                len(device_pks), cluster
            ))
            return redirect(cluster.get_absolute_url())

        return render(request, self.template_name, {
            'cluster': cluster,
            'form': form,
            'return_url': cluster.get_absolute_url(),
        })


### Device Remove
@register_model_view(S3Cluster, 'remove_devices', path='devices/remove')
class S3ClusterRemoveDevicesView(generic.ObjectEditView):
    queryset = S3Cluster.objects.all()
    form = forms.ClusterRemoveDevicesForm
    template_name = 'netbox_object_storage/generic/bulk_remove.html'

    def post(self, request, pk):

        cluster = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            form = self.form(request.POST)
            # if form.is_valid():
            device_pks = request.POST.getlist('pk')
            with transaction.atomic():
                    # Remove the selected Devices from the S3Cluster
                    for device in Device.objects.filter(pk__in=device_pks):
                        cluster.devices.remove(device)
                        cluster.save()

            messages.success(request, "Removed {} devices from S3Cluster {}".format(
                len(device_pks), cluster
            ))
            return redirect(cluster.get_absolute_url())
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = Device.objects.filter(pk__in=pk_values)
        device_table = DeviceTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': cluster,
            'table': device_table,
            'obj_type_plural': 'devices',
            'return_url': cluster.get_absolute_url(),
        })
