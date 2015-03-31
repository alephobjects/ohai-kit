# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ohai_kit.models
from django.conf import settings
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('completion_time', models.DateTimeField(null=True, blank=True)),
                ('batch', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=1, null=True, blank=True)),
                ('pause_total', models.FloatField(null=True, blank=True)),
                ('pause_stamp', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(default=ohai_kit.models.get_uuid, unique=True)),
                ('abstract', models.TextField()),
                ('photo', models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai_kit/static/ohai_kit/'), upload_to=b'uploads', blank=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(default=ohai_kit.models.get_uuid, unique=True)),
                ('abstract', models.TextField()),
                ('photo', models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai_kit/static/ohai_kit/'), upload_to=b'uploads', blank=True)),
                ('order', models.IntegerField(default=0)),
                ('legacy', models.BooleanField(default=False, verbose_name=b'Discontinued Product')),
                ('private', models.BooleanField(default=False)),
                ('index_mode', models.BooleanField(default=False, verbose_name=b'Table of Contents mode?')),
                ('projects', models.ManyToManyField(related_name='project_set', to='ohai_kit.Project', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StepAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai_kit/static/ohai_kit/'), upload_to=b'uploads')),
                ('thumbnail', models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai_kit/static/ohai_kit/'), upload_to=b'uploads', blank=True)),
                ('caption', models.CharField(max_length=500)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StepCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=500)),
                ('check_order', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StepPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai_kit/static/ohai_kit/'), upload_to=b'uploads')),
                ('caption', models.CharField(max_length=500)),
                ('image_order', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completion_time', models.DateTimeField()),
                ('job', models.ForeignKey(to='ohai_kit.JobInstance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('sequence_number', models.IntegerField(default=0)),
                ('project', models.ForeignKey(to='ohai_kit.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='workreceipt',
            name='step',
            field=models.ForeignKey(to='ohai_kit.WorkStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='steppicture',
            name='step',
            field=models.ForeignKey(to='ohai_kit.WorkStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stepcheck',
            name='step',
            field=models.ForeignKey(to='ohai_kit.WorkStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stepattachment',
            name='step',
            field=models.ForeignKey(to='ohai_kit.WorkStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobinstance',
            name='project',
            field=models.ForeignKey(to='ohai_kit.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobinstance',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
