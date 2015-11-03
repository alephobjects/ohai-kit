# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('ohai_kit', '0003_Adding ohai-kit setting database'),
    ]

    operations = [
        migrations.AddField(
            model_name='ohaikitsetting',
            name='force_guest_workflow',
            field=models.BooleanField(default=False, verbose_name=b'Disable jobs and force guest workflow'),
        ),
        migrations.AlterField(
            model_name='ohaikitsetting',
            name='footer_logo',
            field=models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), verbose_name=b'Footer logo image', blank=True),
        ),
        migrations.AlterField(
            model_name='ohaikitsetting',
            name='header_logo',
            field=models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), verbose_name=b'Header logo image', blank=True),
        ),
        migrations.AlterField(
            model_name='ohaikitsetting',
            name='misc_photo',
            field=models.ImageField(upload_to=b'uploads', storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), verbose_name=b'Miscellanous group photo.', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='projectset',
            name='photo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='stepattachment',
            name='attachment',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), upload_to=b'uploads'),
        ),
        migrations.AlterField(
            model_name='stepattachment',
            name='thumbnail',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), upload_to=b'uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='steppicture',
            name='photo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(b'/home/kakaroto/coding/alephobjects/ohai_instance/media/'), upload_to=b'uploads'),
        ),
    ]
