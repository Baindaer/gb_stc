# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0010_auto_20160902_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucion',
            name='fecha_registro',
            field=models.DateTimeField(null=True),
        ),
    ]
