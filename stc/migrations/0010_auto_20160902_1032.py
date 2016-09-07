# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 15:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stc', '0009_auto_20160901_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Causal',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
                ('codigo', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=100)),
                ('grupo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Devolucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_devolucion', models.CharField(max_length=10)),
                ('valor_factura', models.IntegerField()),
                ('detalle', models.CharField(max_length=200)),
                ('fecha_remitido', models.CharField(max_length=10, null=True)),
                ('gestion', models.CharField(max_length=200)),
                ('causal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Causal')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Convenio')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoDV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gestor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RenameField(
            model_name='radicacion',
            old_name='user',
            new_name='usuario',
        ),
        migrations.AlterField(
            model_name='unidad',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.EstadoDV'),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Radicacion'),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='gestor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Gestor'),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='unidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.Unidad'),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
