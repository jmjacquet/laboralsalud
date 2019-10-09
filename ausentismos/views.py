# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext,Context
from django.shortcuts import *
from .models import *
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from django.conf import settings
from general.views import VariablesMixin
# from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from django.utils.decorators import method_decorator
from .forms import AusentismoForm
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId


############ ART ############################

class AusentismoView(VariablesMixin,ListView):
    model = ausentismo
    template_name = 'ausentismos/ausentismo_listado.html'
    context_object_name = 'ausentismo'




class AusentismoCreateView(VariablesMixin,CreateView):
    form_class = AusentismoForm
    template_name = 'ausentismos/ausentismo_form.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_vendedores_abm'):
    #         return redirect(reverse('principal'))
    #     return super(ARTCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(AusentismoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AusentismoCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(AusentismoCreateView, self).get_initial()               
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(AusentismoCreateView, self).form_invalid(form)


class AusentismoEditView(VariablesMixin,UpdateView):
    form_class = AusentismoForm
    model = ausentismo
    pk_url_kwarg = 'id'
    template_name = 'ausentismos/ausentismo_form.html'
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(AusentismoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(AusentismoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(AusentismoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(AusentismoEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(AusentismoEditView, self).get_initial()                      
        return initial            


class AusentismoVerView(VariablesMixin,DetailView):
    model = ausentismo
    pk_url_kwarg = 'id'
    context_object_name = 'ausentismo'
    template_name = 'ausentismos/ausentismo_detalle.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     return super(VendedoresVerView, self).dispatch(*args, **kwargs)        


# @login_required 
def ausentismo_baja_alta(request,id):
    aus = ausentismo.objects.get(pk=id)     
    aus.baja = not aus.baja
    aus.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("ausentismo_listado"))     