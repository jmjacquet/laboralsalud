# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import *
from django.template import RequestContext, Context
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from general.views import VariablesMixin, getVariablesMixin
from laboralsalud.utilidades import usuario_actual, empresa_actual, esAdmin
from modal.views import AjaxUpdateView
from usuarios.forms import *


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
        context['usuarios'] = UsuUsuario.objects.all().order_by('nombre').prefetch_related('permisos')
        return context

@login_required
def UsuarioCreateView(request):    
    if not esAdmin(request):
             return redirect(reverse('principal'))
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
     