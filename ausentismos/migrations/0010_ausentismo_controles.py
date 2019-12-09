# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-12-09 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20191203_2000'),
        ('ausentismos', '0009_auto_20191203_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='ausentismo_controles',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('detalle', models.TextField(blank=True, max_length=500, null=True)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_modif', models.DateField(auto_now=True)),
                ('ausentismo', models.ForeignKey(blank=True, db_column='ausentismo', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='control_ausentismo', to='ausentismos.ausentismo')),
                ('usuario_carga', models.ForeignKey(blank=True, db_column='usuario_carga', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='control_usuario_carga', to='usuarios.UsuUsuario')),
            ],
            options={
                'ordering': ['fecha', 'id'],
                'db_table': 'ausentismo_controles',
            },
        ),
    ]
