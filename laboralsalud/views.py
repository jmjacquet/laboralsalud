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
       
    try:
        empresas = ent_empresa.objects.filter(baja=False)
    except ent_empresa.DoesNotExist:
        empresas = None
 
    # if empresa.mantenimiento == 1:
    #     return render_to_response('mantenimiento.html', {'dirMuni':MUNI_DIR,'sitio':sitio},context_instance=RequestContext(request))
    
    if request.method == 'POST':               
        usuario = request.POST['username']        
        clave = request.POST['password']
        empresa = request.POST['empresa']
        user =  authenticate(usuario=usuario, clave=clave)        
        if user is not None:
          if user.is_active:
            
            django_login(request, user)
            request.session["empresa"] = request.POST['empresa']            
            ROOT_URL = reverse('principal')              

            return HttpResponseRedirect(ROOT_URL)
          else:
          ## invalid login
           error = u"Usuario/Contraseña incorrectos."
        else:
          ## invalid login
           error = u"Usuario/Contraseña incorrectos."
          #return direct_to_template(request, 'invalid_login.html')
    if error:
      messages.add_message(request, messages.ERROR,u'%s' % (error))    
   
    template = 'login.html'      
            
    return render(request,template,{'msj':messages,'empresas':empresas})

def logout(request):
    request.session.clear()
    django_logout(request)
    return HttpResponseRedirect(LOGIN_URL)

def volverHome(request):    
    if not request.user.is_authenticated():
      return HttpResponseRedirect(LOGIN_URL)
    else:
      return HttpResponseRedirect(ROOT_URL)