# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 22:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0028_auto_20160916_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respuesta',
            name='numero',
        ),
    ]