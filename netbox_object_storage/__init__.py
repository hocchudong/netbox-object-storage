from extras.plugins import PluginConfig


class NetBoxManageS3Config(PluginConfig):
    name = 'netbox_object_storage'
    verbose_name = 'Netbox Plugin for Manage S3'
    description = 'Create and Manage S3 in Netbox'
    version = '1.0.0'
    base_url = 'object-storage'
    min_version = '3.4.0'


config = NetBoxManageS3Config