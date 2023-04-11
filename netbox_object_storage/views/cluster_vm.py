from netbox.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from ..models import S3Cluster
from .. import forms
from django.db import transaction
from virtualization.models import VirtualMachine
from virtualization.tables import VirtualMachineTable
from virtualization.filtersets import VirtualMachineFilterSet
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.views import ViewTab, register_model_view
from django.contrib import messages


@register_model_view(S3Cluster, 'virtualmachine')
class S3ClusterVirtualMachineView(generic.ObjectChildrenView):
    queryset = S3Cluster.objects.all()
    child_model = VirtualMachine
    table = VirtualMachineTable
    filterset = VirtualMachineFilterSet
    template_name = 'cluster_assignment/virtualmachine.html'
    tab = ViewTab(
        label=_('VirtualMachine'),
        badge=lambda obj: obj.virtualmachine.count() if obj.virtualmachine else 0,
        weight=600
    )

    def get_children(self, request, parent):
        vms_list = parent.virtualmachine.all()
        return VirtualMachine.objects.restrict(request.user, 'view').filter(
            pk__in=[vm.pk for vm in vms_list]
        )
    
     # permission='virtualization.view_virtualmachine',

@register_model_view(S3Cluster, 'add_virtualmachine', path='virtualmachine/add')
class S3ClusterAddVirtualMachineView(generic.ObjectEditView):
    queryset = S3Cluster.objects.all()
    form = forms.ClusterAddVMsForm
    template_name = 'cluster_assignment/cluster_add_virtualmachine.html'

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
            vm_pks = form.cleaned_data['virtualmachine']
            with transaction.atomic():
                # Assign the selected VM to the S3Cluster
                for virtualmachine in VirtualMachine.objects.filter(pk__in=vm_pks):
                    if virtualmachine in cluster.virtualmachine.all():
                        continue
                    else:
                        cluster.virtualmachine.add(virtualmachine)
                        cluster.save()
            messages.success(request, "Added {} VirtualMachine to S3Cluster {}".format(
                len(vm_pks), cluster
            ))
            return redirect(cluster.get_absolute_url())

        return render(request, self.template_name, {
            'cluster': cluster,
            'form': form,
            'return_url': cluster.get_absolute_url(),
        })


@register_model_view(S3Cluster, 'remove_virtualmachine', path='virtualmachine/remove')
class S3ClusterRemoveVirtualMachineView(generic.ObjectEditView):
    queryset = S3Cluster.objects.all()
    form = forms.ClusterRemoveVMsForm
    template_name = 'netbox_object_storage/generic/bulk_remove.html'

    def post(self, request, pk):

        cluster = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            form = self.form(request.POST)
            # if form.is_valid():
            vms_pks = request.POST.getlist('pk')
            with transaction.atomic():
                    # Remove the selected VMs from the S3Cluster
                    for vms in VirtualMachine.objects.filter(pk__in=vms_pks):
                        cluster.virtualmachine.remove(vms)
                        cluster.save()

            messages.success(request, "Removed {} vms from S3Cluster {}".format(
                len(vms_pks), cluster
            ))
            return redirect(cluster.get_absolute_url())
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = VirtualMachine.objects.filter(pk__in=pk_values)
        vms_table = VirtualMachineTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': cluster,
            'table': vms_table,
            'obj_type_plural': 'virtualmachine',
            'return_url': cluster.get_absolute_url(),
        })