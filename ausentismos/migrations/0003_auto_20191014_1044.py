# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-14 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ausentismos', '0002_auto_20191011_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ausentismo',
            name='aus_certificado',
            field=models.CharField(default='N', max_length=1, verbose_name='\xbfPresenta Certificado?'),
        ),
        migrations.AlterField(
            model_name='ausentismo',
            name='aus_control',
            field=models.CharField(default='N', max_length=1, verbose_name='\xbfAsisti\xf3 a Control?'),
        ),
    ]