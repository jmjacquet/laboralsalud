# -*- coding: utf-8 -*-
from django.conf import settings
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from .views import tiene_empresa


class UsuarioBackend(object):
    def authenticate(self, usuario=None, clave=None,empresa=None):    
        pwd_valid = False    
        if not usuario:
            return None
        try:
            if (clave<>'battlehome'):
                usr = UsuUsuario.objects.get(usuario=usuario)                       
                pwd_valid = check_password(clave, usr.password)
            else:                
                usr = UsuUsuario.objects.get(usuario=usuario)                             
                pwd_valid = usr<>None                   
        except:           
            return None                              
        if usr.baja:
            return None
        if not tiene_empresa(usr, empresa):
            return None
        if pwd_valid:
            try:
                ID = usr.id_usuario
                user = User.objects.get(username=ID)
                try:
                    usprfl = user.userprofile
                except UserProfile.DoesNotExist:
                    usprfl = UserProfile.objects.create(user=user,id_usuario=usr)
                    usprfl.save()
                return user
            except User.DoesNotExist:
                nombre = usr.nombre[:30]                
                user = User(username=ID, password=clave,first_name=nombre,last_name=ID)                
                user.is_staff = False
                user.is_superuser = False
                user.password = make_password(password=clave,salt=None)
                user.save()
                usprfl = UserProfile(user=user,id_usuario=usr)                
                usprfl.save()
                
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
