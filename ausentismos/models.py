# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from laboralsalud.utilidades import *
from entidades.models import ent_empleado,ent_medico_prof


class aus_patologia(models.Model):
    id = models.AutoField(primary_key=True,db_index=True)    
    codigo =  models.CharField(max_length=200)
    patologia =  models.CharField(max_length=200)
    baja = models.BooleanField(default=False)
    class Meta:
        db_table = 'aus_patologia'
    
    def __unicode__(self):
        return u'%s' % (self.patologia)         

    def get_patologia(self):
		entidad=u'%s' % self.patologia.upper()
		if self.codigo:
			entidad = u'%s - ' % (self.codigo)+entidad				
		return entidad.upper()		

class aus_diagnostico(models.Model):
    id = models.AutoField(primary_key=True,db_index=True)    
    codigo =  models.CharField(max_length=200)
    diagnostico =  models.CharField(max_length=200)
    baja = models.BooleanField(default=False)
    class Meta:
        db_table = 'aus_diagnostico'
    
    def __unicode__(self):
        return u'%s' % (self.diagnostico)  
	
	def get_diagnostico(self):
		entidad=u'%s' % self.diagnostico.upper()
		if self.codigo:
			entidad = u'%s - ' % (self.codigo)+entidad		
		return entidad.upper()		               

#Tabla de la Base de Configuracion
class ausentismo(models.Model):	
	empleado = models.ForeignKey(ent_empleado,verbose_name='Empleado',db_column='empleado',blank=True, null=True,related_name='aus_empleado',on_delete=models.SET_NULL)
	tipo_ausentismo = models.IntegerField('Ausentismo',choices=TIPO_AUSENCIA, blank=True, null=True)

	aus_control = models.CharField(u'¿Asistió a Control?',max_length=1,default='N')
	aus_fcontrol = models.DateField(u'Fecha Control',blank=True, null=True)
	aus_certificado = models.CharField(u'¿Presenta Certificado?',max_length=1,default='N')
	aus_fcertif = models.DateField(u'Fecha Certificado',blank=True, null=True)
	aus_fentrega_certif = models.DateField(u'Fecha Entrega Certif.',blank=True, null=True)

	aus_fcrondesde = models.DateField(u'Cronológica Desde',blank=True, null=True)
	aus_fcronhasta = models.DateField(u'Cronológica Hasta',blank=True, null=True)
	aus_diascaidos = models.IntegerField(u'Días Caídos',blank=True, null=True)
	aus_diasjustif = models.IntegerField(u'Días Justif.',blank=True, null=True)
	aus_freintegro = models.DateField(u'Reintegro',blank=True, null=True)
	aus_falta = models.DateField(u'Fecha Alta',blank=True, null=True)
	aus_tipo_alta = models.IntegerField('Tipo Alta',choices=TIPO_ALTA, blank=True, null=True)
	aus_frevision = models.DateField(u'Fecha Revisión',blank=True, null=True)
	aus_medico = models.ForeignKey(ent_medico_prof,verbose_name=u'Médico Tratante',db_column='aus_medico',blank=True, null=True,related_name='aus_medico',on_delete=models.SET_NULL)
	aus_grupop = models.ForeignKey(aus_patologia,verbose_name=u'Grupo Patológico',db_column='aus_grupop',blank=True, null=True,related_name='aus_grupop',on_delete=models.SET_NULL)
	aus_diagn = models.ForeignKey(aus_diagnostico,verbose_name=u'Diagnóstico',db_column='aus_diagn',blank=True, null=True,related_name='aus_diagn',on_delete=models.SET_NULL)

	art_tipo_accidente = models.IntegerField('Tipo Accidente/Enfermedad',choices=TIPO_ACCIDENTE, blank=True, null=True)
	art_ndenuncia = models.CharField(u'Nº Denuncia',max_length=50,blank=True, null=True)
	art_fcontrol = models.DateField(u'Fecha Control',blank=True, null=True)
	art_faccidente = models.DateField(u'Fecha Accidente',blank=True, null=True)
	art_fdenuncia = models.DateField(u'Fecha Denuncia',blank=True, null=True)
	art_fcrondesde = models.DateField(u'Cronológica Desde',blank=True, null=True)
	art_fcronhasta = models.DateField(u'Cronológica Hasta',blank=True, null=True)
	art_diascaidos = models.IntegerField(u'Días Caídos',blank=True, null=True)
	art_freintegro = models.DateField(u'Reintegro',blank=True, null=True)
	art_falta = models.DateField(u'Fecha Alta',blank=True, null=True)
	art_tipo_alta = models.IntegerField('Tipo Alta',choices=TIPO_ALTA, blank=True, null=True)
	art_frevision = models.DateField(u'Fecha Revisión',blank=True, null=True)
	art_medico = models.ForeignKey(ent_medico_prof,verbose_name=u'Médico ART',db_column='art_medico',blank=True, null=True,related_name='art_medico',on_delete=models.SET_NULL)

	observaciones = models.TextField('Observaciones',blank=True, null=True)       
	descr_altaparc = models.TextField(u'Descr.Alta Parcial',blank=True, null=True)       
	detalle_acc_art = models.TextField(u'Detalle Acc.ART',blank=True, null=True)       
	estudios_partic = models.TextField(u'Estudios Particulares',blank=True, null=True)       
	estudios_art = models.TextField(u'Estudios ART',blank=True, null=True)       
	recalificac_art = models.TextField(u'Recalificación ART',blank=True, null=True)       

	baja = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add = True)
	fecha_modif = models.DateTimeField(auto_now = True)			
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='aus_usuario_carga',on_delete=models.SET_NULL)

	class Meta:
		db_table = 'ausentismo'
		ordering = ['empleado']

	def __unicode__(self):
	    return u'%s' % (self.empleado)

	@property
	def get_dias_caidos(self):
		dias = 0
		if self.tipo_ausentismo==1:
			if self.aus_diascaidos:
				dias = self.aus_diascaidos
		else:
			if self.art_diascaidos:
				dias = self.art_diascaidos
		return dias

	@property
	def get_fechas(self):        
		desde=''
		hasta=''
		if self.tipo_ausentismo==1:
			if self.aus_fcrondesde:
				desde = self.aus_fcrondesde.strftime('%d/%m/%Y')		
			if self.aus_fcronhasta:
				hasta = self.aus_fcronhasta.strftime('%d/%m/%Y')
		else:
			if self.art_fcrondesde:
				desde = self.art_fcrondesde.strftime('%d/%m/%Y')		
			if self.art_fcronhasta:
				hasta = self.art_fcronhasta.strftime('%d/%m/%Y')
		return '%s hasta %s' % (desde,hasta)

	




