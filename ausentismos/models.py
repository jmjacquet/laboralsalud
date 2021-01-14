# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from laboralsalud.utilidades import *
from entidades.models import ent_empleado,ent_medico_prof


class aus_patologia(models.Model):
    id = models.AutoField(primary_key=True,db_index=True)    
    codigo =  models.CharField(max_length=200,blank=True, null=True)
    patologia =  models.CharField(max_length=200)
    baja = models.BooleanField(default=False)
    class Meta:
        db_table = 'aus_patologia'
        ordering = ['patologia',]
    
    def __unicode__(self):
        return u'%s' % (self.patologia.upper())         

    def get_patologia(self):
		entidad=u'%s' % self.patologia.upper()	
		return entidad.upper()		

class aus_diagnostico(models.Model):
    id = models.AutoField(primary_key=True,db_index=True)    
    codigo =  models.CharField(max_length=200,blank=True, null=True)
    diagnostico =  models.CharField(max_length=200)
    baja = models.BooleanField(default=False)
    class Meta:
        db_table = 'aus_diagnostico'
        ordering = ['diagnostico',]
    
    def __unicode__(self):
        return u'%s' % (self.diagnostico.upper())  
	
	def get_diagnostico(self):
		entidad=u'%s' % self.diagnostico.upper()		
		return entidad.upper()		               

#Tabla de la Base de Configuracion
class ausentismo(models.Model):	
	empleado = models.ForeignKey('entidades.ent_empleado',verbose_name='Empleado',db_column='empleado',blank=True, null=True,related_name='aus_empleado',on_delete=models.PROTECT)
	tipo_ausentismo = models.IntegerField('Ausentismo',choices=TIPO_AUSENCIA, blank=True, null=True)
	tipo_control = models.CharField('Tipo Control',choices=TIPO_CONTROL, max_length=1,blank=True, null=True)
	
	aus_control = models.CharField(u'¿Asistió a Control?',max_length=1,default='N')
	aus_fcontrol = models.DateField(u'Fecha Próx.Control',blank=True, null=True)
	aus_certificado = models.CharField(u'¿Presenta Certificado?',max_length=1,default='N')
	aus_fcertif = models.DateField(u'Fecha Certificado',blank=True, null=True)
	aus_fentrega_certif = models.DateField(u'Fecha Entrega Certif.',blank=True, null=True)

	aus_fcrondesde = models.DateField(u'Cronológica Desde',blank=True, null=True)
	aus_fcronhasta = models.DateField(u'Cronológica Hasta',blank=True, null=True)
	aus_diascaidos = models.IntegerField(u'Días Caídos',blank=True, null=True)
	aus_diasjustif = models.IntegerField(u'Días Justificados',blank=True, null=True)
	aus_freintegro = models.DateField(u'F.Reintegro',blank=True, null=True)
	aus_falta = models.DateField(u'Fecha Alta',blank=True, null=True)
	aus_tipo_alta = models.IntegerField('Tipo Alta',choices=TIPO_ALTA, blank=True, null=True)
	# aus_frevision = models.DateField(u'Fecha Próx.Control',blank=True, null=True)
	aus_medico = models.ForeignKey('entidades.ent_medico_prof',verbose_name=u'Médico Tratante/ART',db_column='aus_medico',blank=True, null=True,related_name='aus_medico',on_delete=models.SET_NULL)
	aus_grupop = models.ForeignKey(aus_patologia,verbose_name=u'Grupo Patológico',db_column='aus_grupop',blank=True, null=True,related_name='aus_grupop',on_delete=models.SET_NULL)
	aus_diagn = models.ForeignKey(aus_diagnostico,verbose_name=u'Diagnóstico',db_column='aus_diagn',blank=True, null=True,related_name='aus_diagn',on_delete=models.SET_NULL)

	art_tipo_accidente = models.IntegerField('Tipo Accidente/Enfermedad',choices=TIPO_ACCIDENTE, blank=True, null=True)
	art_ndenuncia = models.CharField(u'Nº Denuncia',max_length=50,blank=True, null=True)	
	art_faccidente = models.DateField(u'Fecha Accidente',blank=True, null=True)
	art_fdenuncia = models.DateField(u'Fecha Denuncia',blank=True, null=True)
	
	observaciones = models.TextField('Observaciones',blank=True, null=True)       
	descr_altaparc = models.TextField(u'Descr.Alta Parcial',blank=True, null=True)       
	detalle_acc_art = models.TextField(u'Detalle Acc.ART',blank=True, null=True)       
	estudios_partic = models.TextField(u'Estudios Particulares',blank=True, null=True)       
	estudios_art = models.TextField(u'Estudios ART',blank=True, null=True)       
	recalificac_art = models.TextField(u'Recalificación ART',blank=True, null=True)       

	plan_accion = models.TextField('Observaciones',blank=True, null=True)       

	baja = models.BooleanField(default=False)
	fecha_creacion = models.DateField(auto_now_add = True)
	fecha_modif = models.DateField(auto_now = True)			
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='aus_usuario_carga',on_delete=models.SET_NULL)

	class Meta:
		db_table = 'ausentismo'
		ordering = ['-aus_fcrondesde','-aus_fcronhasta','empleado__empresa']

	def __unicode__(self):
	    return u'%s - %s (%s)' % (self.pk,self.empleado,self.get_fechas)

	@property
	def get_dias_caidos(self):
		dias = 0
		if self.aus_diascaidos:
			dias = self.aus_diascaidos
		return dias

	@property
	def get_fechas(self):        
		desde = None
		hasta = None
		if self.aus_fcrondesde:
			desde=self.aus_fcrondesde.strftime('%d/%m/%Y')
		if self.aus_fcronhasta:
			hasta=self.aus_fcronhasta.strftime('%d/%m/%Y')		
		return '%s hasta %s' % (desde,hasta)

	@property
	def get_fcrondesde(self):
		return self.aus_fcrondesde
				
	@property
	def get_fcronhasta(self):
		return self.aus_fcronhasta		
		
	@property
	def get_proxcontrol(self):
		return self.aus_fcontrol		
		
	@property
	def get_falta(self):
		return self.aus_falta		
		
	@property
	def get_tipo_alta(self):
		return self.get_aus_tipo_alta_display()
	
	@property		
	def get_ultimo_control(self):
		try:
			ultimo = ausentismo_controles.objects.filter(ausentismo=self).order_by('-fecha')[0]
		except:
			return None
		return ultimo
		

class ausentismo_controles(models.Model):
	id = models.AutoField(primary_key=True,db_index=True)
	ausentismo = models.ForeignKey('ausentismo',db_column='ausentismo',related_name='control_ausentismo',blank=True, null=True,on_delete=models.CASCADE)
	fecha = models.DateField(blank=True, null=True)
	detalle = models.TextField(max_length=1000,blank=True, null=True) # Field name made lowercase.   
	fecha_creacion = models.DateField(auto_now_add = True)
	fecha_modif = models.DateField(auto_now = True)			
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='control_usuario_carga',on_delete=models.SET_NULL)    
	class Meta:
	    db_table = 'ausentismo_controles'
	    ordering = ['fecha','id']

	def __unicode__(self):
	    return u'%s - %s' % (self.fecha,self.detalle)

class ausentismo_controles_patologias(models.Model):
	id = models.AutoField(primary_key=True,db_index=True)
	ausentismo = models.ForeignKey('ausentismo',db_column='ausentismo',related_name='control_ausentismo_pat',blank=True, null=True,on_delete=models.CASCADE)
	fecha = models.DateField(blank=True, null=True)
	detalle = models.TextField(max_length=1000,blank=True, null=True) # Field name made lowercase.   
	fecha_creacion = models.DateField(auto_now_add = True)
	fecha_modif = models.DateField(auto_now = True)			
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='control_pat_usuario_carga',on_delete=models.SET_NULL)    
	class Meta:
	    db_table = 'ausentismo_controles_patologias'
	    ordering = ['fecha','id']

	def __unicode__(self):
	    return u'%s - %s' % (self.fecha,self.detalle)

from django.db.models import Q

def ausentismos_del_dia(request,fecha):
	 controles = ausentismo_controles.objects.filter(fecha=fecha).values_list('ausentismo__id', flat=True)	
	 ausentismos = ausentismo.objects.filter(baja=False,empleado__empresa__pk__in=empresas_habilitadas(request))\
	 	.filter(Q(fecha_creacion=fecha)|(Q(id__in=controles)))
	 return ausentismos
     


from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

@receiver(post_save, sender=ausentismo,dispatch_uid="eliminar_controles_vacios")
def eliminar_controles_vacios(sender, instance,created, **kwargs):
   if instance:
   	controles = ausentismo_controles.objects.filter(ausentismo=instance)\
   	.filter(Q(fecha__isnull=True,detalle__isnull=True)|Q(fecha__isnull=True,detalle=''))
   	controles.delete()
   	# if (not instance.fecha)and(not instance.detalle):
   	# 	instance.delete()
