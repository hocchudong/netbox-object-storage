from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_object_storage'

router = NetBoxRouter()
router.register('Pool', views.PoolViewSet)
router.register('Bucket', views.BucketViewSet)
router.register('S3Cluster', views.S3ClusterViewSet)

urlpatterns = router.urls