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


class ARTEditView(VariablesMixin,AjaxUpdateView):
    # form_class = EntidadesEditForm
    model = ent_art
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_clientes_abm'):
    #         return redirect(reverse('principal'))
    #     return super(ARTEditView, self).dispatch(*args, **kwargs)

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