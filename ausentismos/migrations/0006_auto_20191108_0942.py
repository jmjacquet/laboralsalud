# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-08 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ausentismos', '0005_auto_20191104_2234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aus_diagnostico',
            options={'ordering': ['diagnostico']},
        ),
        migrations.AlterModelOptions(
            name='aus_patologia',
            options={'ordering': ['patologia']},
        ),
        migrations.AlterModelOptions(
            name='ausentismo',
            options={'ordering': ['-fecha_creacion', 'empleado__empresa', '-aus_fcrondesde', '-aus_fcronhasta', '-art_fcrondesde', '-art_fcronhasta']},
        ),
    ]