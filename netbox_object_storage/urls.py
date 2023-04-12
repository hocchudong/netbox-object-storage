from django.urls import path

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
        'model': models.Bucket}
    ),

    # # Pool Template
    path('pool/', views.PoolListView.as_view(), name='pool_list'),
    path('pool/add/', views.PoolEditView.as_view(), name='pool_add'),
    path('pool/delete/', views.PoolBulkDeleteView.as_view(), name='pool_bulk_delete'),
    path('pool/<int:pk>/', views.PoolView.as_view(), name='pool'),
    path('pool/<int:pk>/edit/', views.PoolEditView.as_view(), name='pool_edit'),
    path('pool/<int:pk>/delete/', views.PoolDeleteView.as_view(), name='pool_delete'),
    path('pool/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='pool_changelog', kwargs={
        'model': models.Pool
    }),

    # S3Cluster Template
    path('s3cluster/', views.S3ClusterListView.as_view(), name='s3cluster_list'),
    path('s3cluster/add/', views.S3ClusterEditView.as_view(), name='s3cluster_add'),
    path('s3cluster/delete/', views.S3ClusterBulkDeleteView.as_view(), name='s3cluster_bulk_delete'),
    path('s3cluster/<int:pk>/', views.S3ClusterView.as_view(), name='s3cluster'),
    path('s3cluster/<int:pk>/edit/', views.S3ClusterEditView.as_view(), name='s3cluster_edit'),
    path('s3cluster/<int:pk>/delete/', views.S3ClusterDeleteView.as_view(), name='s3cluster_delete'),
    path('s3cluster/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='s3cluster_changelog', kwargs={
        'model': models.S3Cluster
    }),

    # # # S3Cluster device
    path('s3cluster/<int:pk>/devices/', views.S3ClusterDevicesView.as_view(), name='s3cluster_devices'),
    path('s3cluster/<int:pk>/devices/add/', views.S3ClusterAddDevicesView.as_view(), name='s3cluster_add_devices'),
    path('s3cluster/<int:pk>/devices/remove/', views.S3ClusterRemoveDevicesView.as_view(), name='s3cluster_remove_devices'),

    # # S3Cluster vm
    path('s3cluster/<int:pk>/virtualmachine/', views.S3ClusterVirtualMachineView.as_view(), name='s3cluster_virtualmachine'),
    path('s3cluster/<int:pk>/virtualmachine/add/', views.S3ClusterAddVirtualMachineView.as_view(), name='s3cluster_add_virtualmachine'),
    path('s3cluster/<int:pk>/virtualmachine/remove/', views.S3ClusterRemoveVirtualMachineView.as_view(), name='s3cluster_remove_virtualmachine'),
)