# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('ohai_kit', '0002_auto_20150331_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='OhaiKitSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('misc_photo', models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), verbose_name=b'Miscellanous group photo.', blank=True)),
                ('guest_mode', models.BooleanField(default=False, verbose_name=b'Automatically login users as Guest.')),
                ('header_logo', models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), verbose_name=b'Header logo image', blank=True)),
                ('header_logo_alt', models.CharField(default=b'OHAI-Kit', max_length=200, verbose_name=b'Header logo image alternative text')),
                ('header_text', models.CharField(default=b'Open Hardware Assembly Instructions', max_length=200)),
                ('header_description', models.TextField(default=b'OHAI-kit or Open Hardware Assembly Instructions is<br />your one-stop shop for all the User Guides you need.')),
                ('footer_url', models.URLField(default=b'https://code.alephobjects.com/project/profile/9/')),
                ('footer_logo', models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), verbose_name=b'Footer logo image', blank=True)),
                ('footer_logo_alt', models.CharField(default=b'OHAI-Kit', max_length=200, verbose_name=b'Footer logo image alternative text')),
                ('footer_copyleft', models.CharField(default=b'Aleph Objects &mdash; Committed to free and open-source technology.', max_length=200)),
                ('footer_description', models.TextField(default=b'OHAI-kit is free software! Available via <a href="https://code.alephobjects.com/project/profile/9/">Phabricator</a> &amp; <a href="https://github.com/alephobjects/ohai-kit">github</a>')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='projectset',
            name='photo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='stepattachment',
            name='attachment',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), upload_to=b'uploads'),
        ),
        migrations.AlterField(
            model_name='stepattachment',
            name='thumbnail',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='steppicture',
            name='photo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), upload_to=b'uploads'),
        ),
    ]
