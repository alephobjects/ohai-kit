# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ohai_kit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectset',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
    ]
