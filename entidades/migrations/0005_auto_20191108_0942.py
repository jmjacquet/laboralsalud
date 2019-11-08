# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-08 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0004_auto_20191105_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ent_art',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterModelOptions(
            name='ent_cargo',
            options={'ordering': ['cargo']},
        ),
        migrations.AlterModelOptions(
            name='ent_empleado',
            options={'ordering': ['apellido_y_nombre', 'empresa', 'nro_doc']},
        ),
        migrations.AlterModelOptions(
            name='ent_especialidad',
            options={'ordering': ['especialidad']},
        ),
    ]
