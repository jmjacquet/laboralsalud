# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-05 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entidades', '0004_auto_20191105_1210'),
        ('usuarios', '0002_auto_20191023_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='turnos',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True, verbose_name='Fecha Turno')),
                ('detalle', models.CharField(blank=True, max_length=100, null=True, verbose_name='Detalle')),
                ('estado', models.IntegerField(blank=True, choices=[(0, b'PENDIENTE'), (1, b'ATENDIDO'), (2, b'NO ASISTI\xc3\x93')], null=True, verbose_name='Estado')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('baja', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_modif', models.DateField(auto_now=True)),
                ('empleado', models.ForeignKey(blank=True, db_column='empleado', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='turno_empleado', to='entidades.ent_empleado', verbose_name='Empleado')),
                ('usuario_carga', models.ForeignKey(blank=True, db_column='usuario_carga', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='turno_usuario_carga', to='usuarios.UsuUsuario')),
            ],
            options={
                'db_table': 'turnos',
            },
        ),
    ]
