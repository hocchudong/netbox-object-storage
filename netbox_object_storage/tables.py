import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from .models import Pool, Bucket, S3Cluster


__all__ = (
    'PoolTable',
    'BucketTable',
    'S3ClusterTable',
)

class BucketTable(NetBoxTable):
    pk = columns.ToggleColumn()

    name = tables.Column(
        linkify=True,
    )

    capacity = tables.Column()

    contact = tables.Column(
        linkify=True,
    )

    credential = tables.Column()

    url = tables.Column()

    access = ChoiceFieldColumn()

    description = tables.Column()

    assigned_object_type = columns.ContentTypeColumn(
        verbose_name='Storage Backend Type'
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False, 
        verbose_name='Storage Backend'
    )
    
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Bucket
        fields = ("pk", 
                  "id", 
                  "name",
                  "access",
                  "contact",
                  "capacity",
                  "url",
                  "credential",
                  "description", 
                  "comments",
                  "tags", 
                  "assigned_object_type",
                  "assigned_object",
                  "created",
                  "last_updated",
                  "actions",
                )
        default_columns = ("name",
                           "access",
                           "contact",
                           "capacity",
                           "url",
                           "credential",
                           "assigned_object_type",
                           "assigned_object",
                           'actions',
                        )

class PoolTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    type = tables.Column()

    contact = tables.Column(
        linkify=True,
    )

    size = tables.Column()

    cluster = tables.Column(
        linkify=True,
    )

    description = tables.Column()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Pool
        fields = ("pk", 
                  "id", 
                  "name", 
                  "type",
                  "contact",
                  "size",
                  "cluster", 
                  "description", 
                  "comments",
                  "tags", 
                  "created",
                  "last_updated",
                  "actions"
                )
        default_columns = ("name",
                           "type",
                           "contact", 
                           "size",
                           "cluster"
                        )

class S3ClusterTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    type = tables.Column()

    contact = tables.Column(
        linkify=True,
    )

    raw_size = tables.Column()

    used_size = tables.Column()

    dv_count = tables.Column(
        verbose_name='Devices Count',
        accessor='dv_count',
    ) 
    vm_count = tables.Column(
        verbose_name='VM Count',
        accessor='vm_count',
    ) 
    
    description = tables.Column()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
        
    class Meta(NetBoxTable.Meta):
        model = S3Cluster
        fields = ("pk", 
                  "id", 
                  "name", 
                  "type",
                  "raw_size",
                  "used_size",
                  "dv_count",
                  "vm_count",
                  "contact", 
                  "description", 
                  "comments",
                  "tags", 
                  "created",
                  "last_updated",
                  "actions"
                )
        default_columns = ("name",
                           "type",
                           "raw_size",
                           "used_size",
                           "dv_count",
                           "vm_count",
                           "contact",
                           "description", 
                           "tags"
                        )

    # def render_dv_count(self, value):
    #     return value.devices.count()
    
    # def render_dv_count(self, value):
    #     return value.virtualmachine.count()