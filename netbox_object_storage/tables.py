import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from .models import Pool, Bucket, Cluster


__all__ = (
    'PoolTable',
    'BucketTable',
    'ClusterTable',
)

class BucketTable(NetBoxTable):
    pk = columns.ToggleColumn()
    name = tables.Column(
        linkify=True,
    )

    capacity = tables.Column()

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
                  "actions"
                )
        default_columns = ("name",
                           "access",
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

    type = ChoiceFieldColumn()

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
                           "size",
                           "cluster"
                        )

class ClusterTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    type = ChoiceFieldColumn()

    description = tables.Column()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Cluster
        fields = ("pk", 
                  "id", 
                  "name", 
                  "type", 
                  "description", 
                  "comments",
                  "tags", 
                  "created",
                  "last_updated",
                  "actions"
                )
        default_columns = ("name",
                           "type",
                           "description", 
                           "tags"
                        )
