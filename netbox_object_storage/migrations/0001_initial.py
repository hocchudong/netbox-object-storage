# Generated by Django 4.1.5 on 2023-04-06 05:19

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import utilities.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0084_staging'),
        ('virtualization', '0034_standardize_description_comments'),
        ('dcim', '0167_module_status'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(max_length=20, null=True)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('comments', models.TextField(blank=True)),
                ('devices', models.ManyToManyField(blank=True, default=None, related_name='s3cluster_device', to='dcim.device')),
                ('tags', models.ManyToManyField(related_name='s3_clusters', to='taggit.tag')),
                ('virtualmachine', models.ManyToManyField(blank=True, default=None, related_name='s3cluster_vm', to='virtualization.virtualmachine')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=15)),
                ('size', models.IntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('comments', models.TextField(blank=True)),
                ('cluster', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pool_cluster', to='netbox_object_storage.cluster')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, null=True)),
                ('capacity', models.IntegerField(default=0, null=True)),
                ('credential', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=1000, null=True)),
                ('access', models.CharField(blank=True, default='private', max_length=20)),
                ('assigned_object_id', models.PositiveBigIntegerField(blank=True, default=None, null=True)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('comments', models.TextField(blank=True)),
                ('assigned_object_type', models.ForeignKey(default=None, limit_choices_to=models.Q(models.Q(models.Q(('app_label', 'netbox_object_storage'), ('model', 'bucket')), models.Q(('app_label', 'netbox_object_storage'), ('model', 'pool')), _connector='OR')), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contenttypes.contenttype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Bucket',
                'ordering': ('name',),
            },
        ),
        migrations.AddConstraint(
            model_name='bucket',
            constraint=models.UniqueConstraint(fields=('assigned_object_type', 'assigned_object_id'), name='bucket_assigned_object'),
        ),
    ]
