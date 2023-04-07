from django.urls import path, include

from netbox.views.generic import ObjectChangeLogView
from . import models, views

urlpatterns = (

    # Bucket lists
    path('bucket/', views.BucketListView.as_view(), name='bucket_list'),
    path('bucket/add/', views.BucketEditView.as_view(), name='bucket_add'),
    path('bucket/delete/', views.BucketBulkDeleteView.as_view(), name='bucket_bulk_delete'),
    path('bucket/<int:pk>/', views.BucketView.as_view(), name='bucket'),
    path('bucket/<int:pk>/edit/', views.BucketEditView.as_view(), name='bucket_edit'),
    path('bucket/<int:pk>/delete/', views.BucketDeleteView.as_view(), name='bucket_delete'),
    path('bucket/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='bucket_changelog', kwargs={
        'model': models.Bucket
    }),

    # Pool Template
    path('pool/', views.PoolListView.as_view(), name='pool_list'),
    path('pool/add/', views.PoolEditView.as_view(), name='pool_add'),
    path('pool/delete/', views.PoolBulkDeleteView.as_view(), name='pool_bulk_delete'),
    path('pool/<int:pk>/', views.PoolView.as_view(), name='pool'),
    path('pool/<int:pk>/edit/', views.PoolEditView.as_view(), name='pool_edit'),
    path('pool/<int:pk>/delete/', views.PoolDeleteView.as_view(), name='pool_delete'),
    path('pool/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='pool_changelog', kwargs={
        'model': models.Pool
    }),

    # Cluster Template
    path('cluster/', views.ClusterListView.as_view(), name='cluster_list'),
    path('cluster/add/', views.ClusterEditView.as_view(), name='cluster_add'),
    path('cluster/delete/', views.ClusterBulkDeleteView.as_view(), name='cluster_bulk_delete'),
    path('cluster/<int:pk>/', views.ClusterView.as_view(), name='cluster'),
    path('cluster/<int:pk>/edit/', views.ClusterEditView.as_view(), name='cluster_edit'),
    path('cluster/<int:pk>/delete/', views.ClusterDeleteView.as_view(), name='cluster_delete'),
    path('cluster/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='cluster_changelog', kwargs={
        'model': models.Cluster
    }),

    # # Cluster device
    path('cluster/<int:pk>/devices/', views.ClusterDevicesView.as_view(), name='cluster_devices'),
    path('cluster/<int:pk>/devices/add/', views.ClusterAddDevicesView.as_view(), name='cluster_add_devices'),
    path('cluster/<int:pk>/devices/remove/', views.ClusterRemoveDevicesView.as_view(), name='cluster_remove_devices'),

    # # Cluster vm
    path('cluster/<int:pk>/virtualmachine/', views.ClusterVirtualMachineView.as_view(), name='cluster_virtualmachine'),
    path('cluster/<int:pk>/virtualmachine/add/', views.ClusterAddVirtualMachineView.as_view(), name='cluster_add_virtualmachine'),
    path('cluster/<int:pk>/virtualmachine/remove/', views.ClusterRemoveVirtualMachineView.as_view(), name='cluster_remove_virtualmachine'),
)