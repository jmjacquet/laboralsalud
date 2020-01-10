# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from laboralsalud.utilidades import *
from entidades.models import *
import datetime




class turnos(models.Model):
	id = models.AutoField(primary_key=True,db_index=True)    
	empresa = models.ForeignKey('entidades.ent_empresa',verbose_name='Empresa',db_column='empresa',blank=True, null=True,related_name='turno_empresa',on_delete=models.SET_NULL)
	fecha = models.DateField(u'Fecha Turno',blank=True, null=True)
	hora = models.TimeField(u'Hora Turno',blank=True, null=True)
	empleado = models.ForeignKey('entidades.ent_empleado',verbose_name='Empleado',db_column='empleado',blank=True, null=True,related_name='turno_empleado',on_delete=models.SET_NULL)
	detalle = models.CharField(u'Diagnóstico',max_length=100,blank=True, null=True)
	estado = models.IntegerField('Estado',choices=ESTADO_TURNO, blank=True, null=True)
	observaciones = models.TextField('Observaciones',blank=True, null=True)  
	baja = models.BooleanField(default=False)
	fecha_creacion = models.DateField(auto_now_add = True)
	fecha_modif = models.DateField(auto_now = True)			
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='turno_usuario_carga',on_delete=models.SET_NULL)
	class Meta:
	    db_table = 'turnos'
	    ordering = ['fecha','hora','estado']

	def __unicode__(self):
		return u'%s - %s' % (self.fecha.strftime('%d/%m/%Y'),self.empleado)


	def get_turno(self):
		return u'{0:0{width}}'.format(self.pk,width=4)




