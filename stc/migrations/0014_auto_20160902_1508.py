# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0013_auto_20160902_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devolucion',
            name='factura',
            field=models.CharField(max_length=20),
        ),
    ]