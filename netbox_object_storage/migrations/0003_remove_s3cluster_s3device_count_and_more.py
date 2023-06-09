# Generated by Django 4.1.7 on 2023-04-12 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('netbox_object_storage', '0002_remove_pool_contact_remove_s3cluster_contact_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='s3cluster',
            name='s3device_count',
        ),
        migrations.RemoveField(
            model_name='s3cluster',
            name='s3vm_count',
        ),
        migrations.AddField(
            model_name='bucket',
            name='expiration_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='bucket',
            name='issue_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='assigned_object_type',
            field=models.ForeignKey(default=None, limit_choices_to=models.Q(models.Q(models.Q(('app_label', 'netbox_object_storage'), ('model', 's3cluster')), models.Q(('app_label', 'netbox_object_storage'), ('model', 'pool')), _connector='OR')), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contenttypes.contenttype'),
        ),
    ]
