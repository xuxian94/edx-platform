# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletionStatusEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('enterprise_customer_user_id', models.IntegerField()),
                ('sf_user_id', models.CharField(max_length=260)),
                ('course_id', models.CharField(max_length=260)),
                ('course_completed', models.BooleanField(default=True)),
                ('completed_timestamp', models.DateTimeField(auto_now_add=True)),
                ('instructor_name', models.CharField(max_length=260, blank=True)),
                ('grade', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='OCNEnterpriseCustomerConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('enterprise_customer_uuid', models.UUIDField(unique=True)),
                ('sf_base_url', models.CharField(max_length=260)),
                ('provider_slug', models.SlugField(max_length=30)),
                ('key', models.TextField(verbose_name=b'Client ID', blank=True)),
                ('secret', models.TextField(verbose_name=b'Client Secret', blank=True)),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OCNWebServicesConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('completion_status_api_path', models.CharField(max_length=260)),
                ('course_api_path', models.CharField(max_length=260)),
                ('oauth_api_path', models.CharField(max_length=260)),
                ('provider_id', models.CharField(default=b'EDX', max_length=100)),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Changed by')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
    ]
