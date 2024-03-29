# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,date
from django.conf import settings
import os 
from laboralsalud.utilidades import TIPO_USR
from entidades.models import ent_empresa

class UsuCategPermisos(models.Model):
    id = models.AutoField(db_column='ID',primary_key=True) # Field name made lowercase.
    categoria = models.CharField(db_column='CATEGORIA', max_length=100, blank=True, null=True) # Field name made lowercase.
    orden = models.IntegerField(db_column='ORDEN',blank=True, null=True) # Field name made lowercase.    
    class Meta:
        db_table = 'usu_permiso_categ'

    def __unicode__(self):
        return self.categoria
        
class UsuPermiso(models.Model):
    id_permiso = models.AutoField(db_column='ID_PERMISO', primary_key=True) # Field name made lowercase.
    permiso = models.CharField(db_column='PERMISO', max_length=100, blank=True) # Field name made lowercase.    
    permiso_name = models.CharField(db_column='PERMISO_NAME', max_length=100, blank=True) # Field name made lowercase.    
    categoria = models.ForeignKey(UsuCategPermisos, db_column='CATEGORIA', blank=True, null=True,on_delete=models.SET_NULL) # Field name made lowercase.
    class Meta:        
        db_table = 'usu_permiso'

    def __unicode__(self):
        return u'{0}'.format(self.permiso)

        
class UsuUsuario(models.Model):
    id_usuario = models.AutoField(db_column='ID_USUARIO', primary_key=True,unique=True) # Field name made lowercase.    
    nombre = models.CharField(db_column='NOMBRE', max_length=200, blank=True) # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=100, blank=True) # Field name made lowercase.    
    password = models.CharField(db_column='PASSWORD', max_length=100, blank=True) # Field name made lowercase.    
    tipoUsr = models.IntegerField(choices=TIPO_USR,default=0)
    nro_doc = models.CharField(u'Número',max_length=50,blank=True, null=True)               
    email = models.CharField('E-Mail',db_column='EMAIL', max_length=100, blank=True) # Field name made lowercase.
    permisos = models.ManyToManyField(UsuPermiso, related_name='usuario_permisos')
    baja = models.BooleanField(default=False)    
    empresas = models.ManyToManyField(to='entidades.ent_empresa')
    class Meta:
        db_table = 'usu_usuario'

    def __unicode__(self):
        return u'%s' % (self.nombre)

    def get_ultimo_logueo(self):
        usr = UserProfile.objects.get(id_usuario=self.id_usuario).user
        return usr.last_login

#Tabla de Usuario con datos Extra
class UserProfile(models.Model):
    id_usuario = models.ForeignKey(UsuUsuario,db_column='id_usuario',blank=True, null=True,on_delete=models.SET_NULL)
    user = models.OneToOneField(User)

    class Meta:
        db_table = 'usu_profile'

    def __unicode__(self):
        return self.user.username        