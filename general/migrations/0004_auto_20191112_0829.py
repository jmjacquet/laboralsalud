# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-12 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_auto_20191108_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnos',
            name='fecha',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha Turno'),
        ),
    ]