# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ausentismos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ausentismo',
            name='tipo_ausentismo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ausentismo', choices=[(1, b'Inculpable'), (2, b'Accidente'), (3, b'Enfermedad')]),
        ),
    ]
