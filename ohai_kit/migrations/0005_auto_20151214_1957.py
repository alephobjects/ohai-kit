# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('ohai_kit', '0004_auto_20151103_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ohaikitsetting',
            name='footer_logo',
            field=models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), verbose_name=b'Footer logo image', blank=True),
        ),
        migrations.AlterField(
            model_name='ohaikitsetting',
            name='header_logo',
            field=models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), verbose_name=b'Header logo image', blank=True),
        ),
        migrations.AlterField(
            model_name='ohaikitsetting',
            name='misc_photo',
            field=models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai-kit/ohai/media/'), verbose_name=b'Miscellanous group photo.', blank=True),
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
