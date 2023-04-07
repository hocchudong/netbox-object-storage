from django.db.models import Q

BUCKET_ASSIGNMENT_MODELS = Q(
    Q(app_label='netbox_object_storage', model='bucket') |
    Q(app_label='netbox_object_storage', model='pool')
)