# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from laboralsalud.utilidades import *
from usuarios.models import *

class ent_cargo(models.Model):
    id = models.AutoField(primary_key=True,db_index=True)    
    cargo =  models.CharField(max_length=200)
    baja = models.BooleanField(default=False)
    class Meta:
        db_table = 'ent_cargo'
    
    def __unicode__(self):
        return u'%s' % self.cargo

class ent_especialidad(models.Model):
    id = models.AutoField(primary_key=True,db_index=True)    
    especialidad =  models.CharField(max_length=200)
    baja = models.BooleanField(default=False)
    class Meta:
        db_table = 'ent_especialidad'
    
    def __unicode__(self):
        return u'%s' % self.especialidad 

class ent_empresa(models.Model):
	razon_social = models.CharField(u'Razón Social',max_length=200,blank=True, null=True)	
	cuit = models.CharField('CUIT',max_length=50,blank=True, null=True)   
	direccion = models.CharField(u'Dirección',max_length=200,blank=True, null=True)   
	telefono = models.CharField(u'Teléfono',max_length=50,blank=True, null=True)   
	categFiscal = models.IntegerField(u'Categoría Fiscal',choices=CATEG_FISCAL, blank=True, null=True)   
	codigo = models.CharField(u'Código',max_length=50,blank=True, null=True)   
	iibb = models.CharField(u'Nº IIBB',max_length=50,blank=True, null=True)
	fecha_inicio_activ = models.DateTimeField('Fecha Inicio Actividades',null=True)
	domicilio = models.CharField('Domicilio',max_length=200,blank=True, null=True)   
	provincia = models.IntegerField('Provincia',choices=PROVINCIAS, blank=True, null=True,default=12)
	localidad = models.CharField('Localidad',max_length=100,blank=True, null=True)   
	cod_postal = models.CharField('CP',max_length=50,blank=True, null=True)
	email = models.EmailField('Email')
	telefono = models.CharField(u'Teléfono',max_length=50,blank=True, null=True)   
	celular = models.CharField('Celular',max_length=50,blank=True, null=True)   
	baja = models.BooleanField(default=False)
	fecha_creacion = models.DateField(auto_now_add = True)    
	fecha_modif = models.DateTimeField(auto_now = True)	
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='empr_usuario_carga',on_delete=models.SET_NULL)

	rubro =  models.CharField(u'Rubro',max_length=200,blank=True, null=True)   
	cant_empleados = models.IntegerField(u'DireCant.Empleados',blank=True, null=True)   
	art = models.ForeignKey('ent_art',db_column='art',blank=True, null=True,related_name='empr_art',on_delete=models.SET_NULL)
	medico_prof = models.ForeignKey('ent_medico_prof',db_column='medico_prof',blank=True, null=True,related_name='empr_medico_prof',on_delete=models.SET_NULL)

	casa_central = models.ForeignKey('ent_empresa',db_column='casa_central',blank=True, null=True,related_name='empr_casa_central',on_delete=models.SET_NULL)

	contacto_nombre=models.CharField('Contacto Nombre',max_length=200,blank=True, null=True)   
	contacto_email=models.EmailField('contacto Email',blank=True, null=True)
	contacto_tel=models.CharField(u'Teléfono',max_length=50,blank=True, null=True)   
	contacto_cargo = models.ForeignKey('ent_cargo',db_column='cargo',blank=True, null=True,related_name='empr_cargo',on_delete=models.SET_NULL)
	contacto_profesion = models.ForeignKey('ent_especialidad',db_column='especialidad',blank=True, null=True,related_name='empr_especialidad',on_delete=models.SET_NULL)
	class Meta:
		db_table = 'ent_empresa'
		ordering = ['razon_social','cuit']

#Tabla de la Base de Configuracion
class ent_medico_prof(models.Model):	
	apellido_y_nombre =  models.CharField('Apellido y Nombre',max_length=200)   
	codigo = models.CharField(u'Código',max_length=50,blank=True, null=True)   	
	cuit = models.CharField('CUIT',max_length=50,blank=True, null=True)
	nro_doc = models.CharField(u'Documento',max_length=50,blank=True, null=True)   	
	domicilio = models.CharField('Domicilio',max_length=200,blank=True, null=True)   
	provincia = models.IntegerField('Provincia',choices=PROVINCIAS, blank=True, null=True,default=12)
	localidad = models.CharField('Localidad',max_length=100,blank=True, null=True)   
	cod_postal = models.CharField('CP',max_length=50,blank=True, null=True)
	email = models.EmailField('Email',blank=True)
	telefono = models.CharField(u'Teléfono',max_length=50,blank=True, null=True)   
	celular = models.CharField('Celular',max_length=50,blank=True, null=True)   	
	especialidad = models.ForeignKey('ent_especialidad',db_column='especialidad',blank=True, null=True,related_name='med_especialidad',on_delete=models.SET_NULL)
	observaciones = models.TextField('Observaciones',blank=True, null=True)       
	baja = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add = True)
	fecha_modif = models.DateTimeField(auto_now = True)			
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='med_usuario_carga',on_delete=models.SET_NULL)
		
	class Meta:
		db_table = 'ent_medico_prof'
		ordering = ['apellido_y_nombre','codigo']
		
class ent_art(models.Model):    
	codigo = models.CharField(u'Código',max_length=50,blank=True, null=True)   
	nombre = models.CharField(u'Nombre',max_length=500, blank=True, null=True) # Field name made lowercase.    
	prestador = models.CharField('Prestador',max_length=500, blank=True, null=True)
	auditor = models.CharField('Auditor',max_length=500, blank=True, null=True)
	contacto_nombre = models.CharField('Nombre',max_length=500, blank=True, null=True)
	contacto_telfijo = models.CharField('Tel.Fijo',max_length=100, blank=True, null=True)
	contacto_telcel = models.CharField('Celular',max_length=100, blank=True, null=True)
	contacto_email = models.EmailField('Email',blank=True)
	baja = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add = True)
	fecha_modif = models.DateTimeField(auto_now = True)
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='art_usuario_carga',on_delete=models.SET_NULL)
	class Meta:
	    db_table = 'ent_art'

	def __unicode__(self):
	    return u'%s' % (self.nombre)
	
#Tabla de la Base de Configuracion
class ent_empleado(models.Model):	
	nro_doc = models.CharField(u'Documento',max_length=50,blank=True, null=True)
	legajo = models.CharField(u'Legajo',max_length=50,blank=True, null=True)   	
	apellido = models.CharField('Apellido',max_length=200)   
	nombre =  models.CharField('Nombre',max_length=200)   
	fecha_nac = models.DateField(blank=True, null=True)
	domicilio = models.CharField('Domicilio',max_length=200,blank=True, null=True)   
	provincia = models.IntegerField('Provincia',choices=PROVINCIAS, blank=True, null=True,default=12)
	localidad = models.CharField('Localidad',max_length=100,blank=True, null=True)   
	cod_postal = models.CharField('CP',max_length=50,blank=True, null=True)
	email = models.EmailField('Email',blank=True)
	telefono = models.CharField(u'Teléfono',max_length=50,blank=True, null=True)   
	celular = models.CharField('Celular',max_length=50,blank=True, null=True)   
	art = models.ForeignKey('ent_art',db_column='art',blank=True, null=True,related_name='empl_art',on_delete=models.SET_NULL)

	empresa = models.ForeignKey('ent_empresa',db_column='empresa',blank=True, null=True,related_name='empl_empresa',on_delete=models.SET_NULL)
	empr_fingreso = models.DateField(blank=True, null=True)	
	trab_cargo = models.ForeignKey('ent_cargo',db_column='cargo',blank=True, null=True,related_name='empl_cargo',on_delete=models.SET_NULL)
	trab_fingreso = models.DateField(blank=True, null=True)
	trab_fbaja = models.DateField(blank=True, null=True)

	trab_armas = models.BooleanField(default=False)
	trab_tareas_dif = models.BooleanField(default=False)
	trab_preocupac = models.BooleanField(default=False)
	trab_preocup_fecha = models.DateField(blank=True, null=True)

	trab_preocup_conclus = models.TextField(u'Conclusión Preocupacional',blank=True, null=True) 
	trab_factores_riesgo = models.TextField(u'Factores de Riesgo a lo que está Expuesto',blank=True, null=True) 
	trab_tareas_dif = models.TextField(u'Descripción Tareas Diferentes',blank=True, null=True) 
	trab_anteriores = models.TextField(u'Trabajos Anteriores',blank=True, null=True) 
	trab_antecedentes = models.TextField(u'Antecedentes Patológicos',blank=True, null=True) 
	trab_accidentes = models.TextField(u'Accidentes ART',blank=True, null=True) 
	trab_vacunas = models.TextField(u'Vacunas',blank=True, null=True) 

	observaciones = models.TextField('Observaciones',blank=True, null=True)       
	baja = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add = True)
	fecha_modif = models.DateTimeField(auto_now = True)			
	usuario_carga = models.ForeignKey('usuarios.UsuUsuario',db_column='usuario_carga',blank=True, null=True,related_name='empl_usuario_carga',on_delete=models.SET_NULL)

	class Meta:
		db_table = 'ent_empleado'
		ordering = ['apellido','nombre']