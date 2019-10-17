# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.template import RequestContext,Context
from django.shortcuts import *
from .models import *
from django.contrib.auth.decorators import login_required
from fm.views import AjaxDeleteView
from django.views.generic import TemplateView,ListView,CreateView,UpdateView
from .forms import *

@login_required 
def ver_permisos(request):
    try:
        if request:
            usuario=request.user.userprofile.id_usuario           
            if usuario.grupo.pk == 0:
                permisos = UsuPermiso.objects.all().values_list('permiso_name', flat=True).distinct()
            else:
                # permisos = UsuPermiso.objects.filter(grupo=usuario.grupo).values_list('permiso_name', flat=True).distinct()               
                permisos = usuario.permisos.values_list('permiso_name', flat=True).distinct()
        else:
            permisos = []
    except:
        permisos = []
    
    return permisos  

@login_required 
def tiene_permiso(request,permiso):
    permisos = ver_permisos(request)        
    return (permiso in permisos)


from django.contrib.auth.hashers import make_password

# @login_required 
def password(request):
  if request.method == 'GET':
    clave = request.GET.get('clave','')
    if clave:
      clave = make_password(password=clave,salt=None)

  return HttpResponse( clave, content_type='application/json' ) 

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

@login_required 
def cambiar_password(request):            
    form = UsuarioCambiarPasswdForm(request.POST or None)
    if request.method == 'POST' and request.is_ajax():                                       
        if form.is_valid():                                   
            new_password = form.cleaned_data['new_password']
            usuario=request.user.userprofile.id_usuario
            clave = make_password(password=new_password,salt=None)
            usuario.password = clave
            usuario.save()
            update_session_auth_hash(request, usuario)            
            response = {'status': 1, 'message': "Ok"} # for ok        
        else:
            errors = form.errors            
            response = {'status': 0, 'message': json.dumps(errors)} 
            
        return HttpResponse(json.dumps(response,default=default), content_type='application/json')
    else:                
        variables = RequestContext(request, {'form':form})        
        return render_to_response("general/cambiar_password.html", variables)
