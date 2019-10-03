# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext,Context
from django.shortcuts import *
from .models import *
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from django.conf import settings
from general.views import VariablesMixin
from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from django.utils.decorators import method_decorator
from .forms import ARTForm
from django.contrib import messages


class ARTView(VariablesMixin,ListView):
    model = ent_art
    template_name = 'entidades/art_listado.html'
    context_object_name = 'art'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_clientes'):
    #         return redirect(reverse('principal'))
    #     return super(ARTView, self).dispatch(*args, **kwargs)

    def get_queryset(self):        
        entidades = ent_art.objects.all()
        # usuario = usuario_actual(self.request)
        # if habilitado_contador(usuario.tipoUsr):
        #     entidades = egr_entidad.objects.filter(tipo_entidad=1,empresa__id__in=empresas_habilitadas(self.request))
        return entidades

class ARTCreateView(VariablesMixin,AjaxCreateView):
    form_class = ARTForm
    template_name = 'fm/entidades/form_art.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_vendedores_abm'):
    #         return redirect(reverse('principal'))
    #     return super(ARTCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(ARTCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ARTCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(ARTCreateView, self).get_initial()               
        # initial['codigo'] = '{0:0{width}}'.format((ultimoNroId(egr_entidad)+1),width=4)
        # initial['tipo_entidad'] = 3
        # initial['empresa'] = empresa_actual(self.request)
        initial['request'] = self.request        
        return initial    


class ARTEditView(VariablesMixin,AjaxUpdateView):
    form_class = ARTForm
    model = ent_art
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_art.html'
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(ARTEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(ARTEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ARTEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(ARTEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(ARTEditView, self).get_initial()                      
        return initial            


class ARTVerView(VariablesMixin,DetailView):
    model = ent_art
    pk_url_kwarg = 'id'
    context_object_name = 'art'
    template_name = 'entidades/art_detalle.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     return super(VendedoresVerView, self).dispatch(*args, **kwargs)        


# @login_required 
def art_baja_alta(request,id):
    art = ent_art.objects.get(pk=id)     
    art.baja = not art.baja
    art.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("art_listado")) 