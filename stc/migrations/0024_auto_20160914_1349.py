# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-14 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0023_glosa_fecha_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='fecha_registro',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='respuestaratificacion',
            name='fecha_registro',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='fecha_respuesta',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='respuestaratificacion',
            name='fecha_respuesta',
            field=models.DateField(),
        ),
    ]
