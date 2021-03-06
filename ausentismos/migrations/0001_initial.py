# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-01-14 11:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entidades', '__first__'),
        ('usuarios', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='aus_diagnostico',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('codigo', models.CharField(blank=True, max_length=200, null=True)),
                ('diagnostico', models.CharField(max_length=200)),
                ('baja', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['diagnostico'],
                'db_table': 'aus_diagnostico',
            },
        ),
        migrations.CreateModel(
            name='aus_patologia',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('codigo', models.CharField(blank=True, max_length=200, null=True)),
                ('patologia', models.CharField(max_length=200)),
                ('baja', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['patologia'],
                'db_table': 'aus_patologia',
            },
        ),
        migrations.CreateModel(
            name='ausentismo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ausentismo', models.IntegerField(blank=True, choices=[(1, b'Inculpable'), (2, b'Accidente'), (3, b'Enfermedad Profesional'), (4, b'Familiar Enfermo')], null=True, verbose_name='Ausentismo')),
                ('tipo_control', models.CharField(blank=True, choices=[(b'C', b'Consultorio'), (b'D', b'Domicilio')], max_length=1, null=True, verbose_name='Tipo Control')),
                ('aus_control', models.CharField(default='N', max_length=1, verbose_name='\xbfAsisti\xf3 a Control?')),
                ('aus_fcontrol', models.DateField(blank=True, null=True, verbose_name='Fecha Pr\xf3x.Control')),
                ('aus_certificado', models.CharField(default='N', max_length=1, verbose_name='\xbfPresenta Certificado?')),
                ('aus_fcertif', models.DateField(blank=True, null=True, verbose_name='Fecha Certificado')),
                ('aus_fentrega_certif', models.DateField(blank=True, null=True, verbose_name='Fecha Entrega Certif.')),
                ('aus_fcrondesde', models.DateField(blank=True, null=True, verbose_name='Cronol\xf3gica Desde')),
                ('aus_fcronhasta', models.DateField(blank=True, null=True, verbose_name='Cronol\xf3gica Hasta')),
                ('aus_diascaidos', models.IntegerField(blank=True, null=True, verbose_name='D\xedas Ca\xeddos')),
                ('aus_diasjustif', models.IntegerField(blank=True, null=True, verbose_name='D\xedas Justificados')),
                ('aus_freintegro', models.DateField(blank=True, null=True, verbose_name='F.Reintegro')),
                ('aus_falta', models.DateField(blank=True, null=True, verbose_name='Fecha Alta')),
                ('aus_tipo_alta', models.IntegerField(blank=True, choices=[(0, b'En Curso'), (1, b'Definitiva'), (2, 'Con Restricci\xf3n')], null=True, verbose_name='Tipo Alta')),
                ('art_tipo_accidente', models.IntegerField(blank=True, choices=[(1, 'En Ocasi\xf3n de Trabajo'), (2, 'In It\xednere')], null=True, verbose_name='Tipo Accidente/Enfermedad')),
                ('art_ndenuncia', models.CharField(blank=True, max_length=50, null=True, verbose_name='N\xba Denuncia')),
                ('art_faccidente', models.DateField(blank=True, null=True, verbose_name='Fecha Accidente')),
                ('art_fdenuncia', models.DateField(blank=True, null=True, verbose_name='Fecha Denuncia')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('descr_altaparc', models.TextField(blank=True, null=True, verbose_name='Descr.Alta Parcial')),
                ('detalle_acc_art', models.TextField(blank=True, null=True, verbose_name='Detalle Acc.ART')),
                ('estudios_partic', models.TextField(blank=True, null=True, verbose_name='Estudios Particulares')),
                ('estudios_art', models.TextField(blank=True, null=True, verbose_name='Estudios ART')),
                ('recalificac_art', models.TextField(blank=True, null=True, verbose_name='Recalificaci\xf3n ART')),
                ('baja', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_modif', models.DateField(auto_now=True)),
                ('aus_diagn', models.ForeignKey(blank=True, db_column='aus_diagn', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aus_diagn', to='ausentismos.aus_diagnostico', verbose_name='Diagn\xf3stico')),
                ('aus_grupop', models.ForeignKey(blank=True, db_column='aus_grupop', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aus_grupop', to='ausentismos.aus_patologia', verbose_name='Grupo Patol\xf3gico')),
                ('aus_medico', models.ForeignKey(blank=True, db_column='aus_medico', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aus_medico', to='entidades.ent_medico_prof', verbose_name='M\xe9dico Tratante/ART')),
                ('empleado', models.ForeignKey(blank=True, db_column='empleado', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='aus_empleado', to='entidades.ent_empleado', verbose_name='Empleado')),
                ('usuario_carga', models.ForeignKey(blank=True, db_column='usuario_carga', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aus_usuario_carga', to='usuarios.UsuUsuario')),
            ],
            options={
                'ordering': ['-aus_fcrondesde', '-aus_fcronhasta', 'empleado__empresa'],
                'db_table': 'ausentismo',
            },
        ),
        migrations.CreateModel(
            name='ausentismo_controles',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('detalle', models.TextField(blank=True, max_length=1000, null=True)),
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
