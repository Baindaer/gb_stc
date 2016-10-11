# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 20:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stc', '0030_auto_20161003_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
