# -*- coding: utf-8 -*-
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.shortcuts import *
from settings import *
from django.core.urlresolvers import reverse
from django.contrib import messages
from entidades.models import ent_empresa
from usuarios.models import UserProfile
from django.db.models import Q
from django.template.defaulttags import register
from .utilidades import usuario_actual
from general.forms import LoginForm
LOGIN_URL = '/login/'
ROOT_URL = '/'

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def login(request):
    error = None
    ROOT_URL='/'
    request.session.clear()
    if request.user.is_authenticated():
      return HttpResponseRedirect(ROOT_URL)
       
    form = LoginForm(request.POST or None) 
    # if empresa.mantenimiento == 1:
    #     return render_to_response('mantenimiento.html', {'dirMuni':MUNI_DIR,'sitio':sitio},context_instance=RequestContext(request))
    
    if form.is_valid():                
        usuario = form.cleaned_data['usuario']        
        clave = form.cleaned_data['password']
        empresa = form.cleaned_data['empresa']
        user =  authenticate(usuario=usuario, clave=clave,empresa=empresa)        
        if user is not None:
          if user.is_active:                        
            django_login(request, user)            
            if empresa:
              request.session["empresa"] = empresa.pk       
            ROOT_URL = reverse('principal')              
            return HttpResponseRedirect(ROOT_URL)
          else:
          ## invalid login
           error = u"Usuario/Contraseña/Empresa incorrectos."
        else:
          ## invalid login
           error = u"Usuario/Contraseña/Empresa incorrectos."
          #return direct_to_template(request, 'invalid_login.html')
    if error:
      messages.add_message(request, messages.ERROR,u'%s' % (error))    
   
    template = 'login.html'      
            
    return render(request,template,{'msj':messages,'form':form})

def logout(request):
    request.session.clear()
    django_logout(request)
    return HttpResponseRedirect(LOGIN_URL)

def volverHome(request):    
    if not request.user.is_authenticated():
      return HttpResponseRedirect(LOGIN_URL)
    else:
      return HttpResponseRedirect(ROOT_URL)