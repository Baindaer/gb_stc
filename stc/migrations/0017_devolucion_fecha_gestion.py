# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-06 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0016_auto_20160902_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucion',
            name='fecha_gestion',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
