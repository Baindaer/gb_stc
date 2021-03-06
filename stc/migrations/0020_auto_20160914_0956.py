# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-14 14:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stc', '0019_auto_20160912_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoGL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Glosa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factura', models.CharField(max_length=20)),
                ('fecha_glosa', models.CharField(max_length=10)),
                ('valor_factura', models.IntegerField()),
                ('valor_glosa', models.IntegerField()),
                ('saldo_glosa', models.IntegerField()),
                ('fecha_respuesta_lim', models.CharField(max_length=10)),
                ('detalle', models.CharField(max_length=250)),
                ('fecha_remitido', models.CharField(max_length=10, null=True)),
                ('fecha_ratificacion', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('glosa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stc.Glosa')),
                ('numero', models.IntegerField()),
                ('fecha_respuesta', models.CharField(max_length=10)),
                ('gestion', models.CharField(max_length=250)),
                ('aceptado_ips', models.IntegerField()),
                ('referencia', models.CharField(max_length=250, null=True)),
                ('codigo_respuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Causal')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaRatificacion',
            fields=[
                ('glosa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stc.Glosa')),
                ('numero', models.IntegerField()),
                ('fecha_respuesta', models.CharField(max_length=10)),
                ('gestion', models.CharField(max_length=250)),
                ('aceptado_ips', models.IntegerField()),
                ('referencia', models.CharField(max_length=250, null=True)),
                ('codigo_respuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Causal')),
            ],
        ),
        migrations.AddField(
            model_name='glosa',
            name='causal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Causal'),
        ),
        migrations.AddField(
            model_name='glosa',
            name='convenio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Convenio'),
        ),
        migrations.AddField(
            model_name='glosa',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Empresa'),
        ),
        migrations.AddField(
            model_name='glosa',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.EstadoGL'),
        ),
        migrations.AddField(
            model_name='glosa',
            name='gestor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Gestor'),
        ),
        migrations.AddField(
            model_name='glosa',
            name='unidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Unidad'),
        ),
        migrations.AddField(
            model_name='glosa',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
