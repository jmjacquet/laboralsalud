# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *
from django.template import RequestContext,Context
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView,CreateView,UpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
import json

from modal.views import AjaxDeleteView,AjaxUpdateView
from .models import *
from .forms import *
from laboralsalud.utilidades import hoy, usuario_actual, empresa_actual, esAdmin, empresa_y_sucursales
from general.views import VariablesMixin

@login_required 
def ver_permisos(request):
    try:
        if request:
            usuario=usuario_actual(request)      
            if usuario.tipoUsr == 0:
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

 
def tiene_empresa(usuario, empresa):
    if usuario:
        if usuario.tipoUsr == 0:
            return True
        else:                        
            if empresa:
                empr_elegidas = empresa_y_sucursales(empresa.id)
                usr_empresas = usuario.empresas.values_list('id', flat=True).distinct()
                return any(e in usr_empresas for e in empr_elegidas)
            else:
                return False
    return False

# @login_required 
def password(request):
  if request.method == 'GET':
    clave = request.GET.get('clave','')
    if clave:
      clave = make_password(password=clave,salt=None)

  return HttpResponse( clave, content_type='application/json' ) 

def unpassword(request):
  if request.method == 'GET':
    clave = request.GET.get('clave','')
    if clave:
      clave = make_password(password=clave,salt=None)

  return HttpResponse( clave, content_type='application/json' ) 

class cambiar_password(VariablesMixin,AjaxUpdateView):
    form_class = UsuarioCambiarPasswdForm
    model = UsuUsuario
    pk_url_kwarg = 'id'
    template_name = 'modal/general/form_cambiar_passwd.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):         
        return super(cambiar_password, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        new_password = form.cleaned_data['password'].replace(" ", "")
        usuario=self.object
        usuario2=self.request.user.userprofile.id_usuario                
        if usuario!=usuario2:
            messages.error(self.request, u'No puede modificar la contraseña de otro usuario!')
            return redirect(reverse('principal'))
        clave = make_password(password=new_password,salt=None)
        usuario.password = clave
        usuario.save()
        update_session_auth_hash(self.request, usuario)            
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(cambiar_password, self).form_valid(form)

    def form_invalid(self, form):
        return super(cambiar_password, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(cambiar_password, self).get_form_kwargs()        
        return kwargs  

    def get_initial(self):    
        initial = super(cambiar_password, self).get_initial()                      
        return initial   

# def cambiar_password(request):                
#     form = UsuarioCambiarPasswdForm(request.POST or None)
#     if request.method == 'POST' and request.is_ajax():                                       
#         if form.is_valid():                                   
#             new_password = form.cleaned_data['new_password']
#             usuario=request.user.userprofile.id_usuario
#             clave = make_password(password=new_password,salt=None)
#             usuario.password = clave
#             usuario.save()
#             update_session_auth_hash(request, usuario)            
#             response = {'status': 1, 'message': "Ok"} # for ok        
#         else:
#             errors = form.errors            
#             response = {'status': 0, 'message': json.dumps(errors)} 
            
#         return HttpResponse(json.dumps(response), content_type='application/json')
#     else:                
#         return render(request,"usuarios/cambiar_password.html",{'form':form})

from general.views import VariablesMixin,getVariablesMixin

class UsuarioList(VariablesMixin,ListView):
    template_name = 'usuarios/usuario_listado.html'
    model = UsuUsuario
    context_object_name = 'usuarios'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                
        if not esAdmin(self.request):
             return redirect(reverse('principal'))
        return super(UsuarioList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsuarioList, self).get_context_data(**kwargs)        
        context['usuarios'] = UsuUsuario.objects.all().order_by('nombre')      
        return context

@login_required
def UsuarioCreateView(request):    
    if not esAdmin(request):
             return redirect(reverse('principal'))
    context = {}
    context = getVariablesMixin(request)    
    try:
        empresa = empresa_actual(request)
    except gral_empresa.DoesNotExist:
        empresa = None 
      
    usuario = usuario_actual(request)
    if request.method == 'POST':
        form = UsuarioForm(request,usuario,request.POST,request.FILES)
        if form.is_valid():
            form.instance.password = make_password(password=form.instance.usuario,salt=None)
            post = form.save(commit=False)                                    
            post.save()
            form.save_m2m()                            
            
            messages.success(request, u'Los datos se guardaron con éxito!')
            return HttpResponseRedirect(reverse('usuarios'))  
    else:
        form = UsuarioForm(request,usuario=usuario)

    context['form'] = form
    return render(request, 'usuarios/usuario_form.html',context)

@login_required
def UsuarioEditView(request,id):
    if not esAdmin(request):
             return redirect(reverse('principal'))
    context = {}
    context = getVariablesMixin(request)
    usuario = usuario_actual(request)
    usr = get_object_or_404(UsuUsuario, id_usuario=id)
    if request.method == 'POST':
        form = UsuarioForm(request,usuario,request.POST,request.FILES,instance=usr)
        if form.is_valid():
            post = form.save(commit=False)                                    
            post.save()
            form.save_m2m()
            messages.success(request, u'Los datos se guardaron con éxito!')
            return HttpResponseRedirect(reverse('usuarios'))                    
    else:
        form = UsuarioForm(request,usuario,instance=usr)

    context['form'] = form
    return render(request, 'usuarios/usuario_form.html',context)


@login_required
def usuarios_baja_reactivar(request,id):
    if not esAdmin(request):
             return redirect(reverse('principal'))
    usr = UsuUsuario.objects.get(pk=id) 
    usr.baja = not usr.baja
    usr.save()  
    messages.success(request, u'Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse('usuarios'))  

@login_required
def usuarios_resetear_passwd(request,id):    
    if not esAdmin(request):
             return redirect(reverse('principal'))
    usuario = UsuUsuario.objects.get(pk=id) 
    clave = make_password(password=usuario.usuario, salt=None)
    usuario.password = clave
    usuario.save()
    messages.success(request, u'Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse('usuarios'))  
     