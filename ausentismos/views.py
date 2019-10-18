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
from .forms import AusentismoForm,PatologiaForm
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId,usuario_actual
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView

############ aus_patologia ############################

class PatologiaView(VariablesMixin,ListView):
    model = aus_patologia
    template_name = 'ausentismos/patologia_listado.html'
    context_object_name = 'patologias'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(PatologiaView, self).dispatch(*args, **kwargs)
    

class PatologiaCreateView(VariablesMixin,AjaxCreateView):
    form_class = PatologiaForm
    template_name = 'fm/entidades/form_patologia.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_vendedores_abm'):
        #     return redirect(reverse('principal'))
        return super(PatologiaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(PatologiaCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PatologiaCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(PatologiaCreateView, self).get_initial()               
        # initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(aus_patologia)+1),width=4)
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(PatologiaCreateView, self).form_invalid(form)


class PatologiaEditView(VariablesMixin,AjaxUpdateView):
    form_class = PatologiaForm
    model = aus_patologia
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_patologia.html'
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(PatologiaEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(PatologiaEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PatologiaEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(PatologiaEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(PatologiaEditView, self).get_initial()                      
        return initial            


# class PatologiaVerView(VariablesMixin,DetailView):
#     model = ent_art
#     pk_url_kwarg = 'id'
#     context_object_name = 'art'
#     template_name = 'entidades/art_detalle.html'

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs): 
#         return super(ARTVerView, self).dispatch(*args, **kwargs)        


# @login_required 
# def art_baja_alta(request,id):
#     art = ent_art.objects.get(pk=id)     
#     art.baja = not art.baja
#     art.save()       
#     messages.success(request, u'¡Los datos se guardaron con éxito!')
#     return HttpResponseRedirect(reverse("art_listado")) 




############ ART ############################

class AusentismoView(VariablesMixin,ListView):
    model = ausentismo
    template_name = 'ausentismos/ausentismo_listado.html'
    context_object_name = 'ausentismo'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(AusentismoView, self).dispatch(*args, **kwargs)

class AusentismoCreateView(VariablesMixin,CreateView):
    form_class = AusentismoForm
    template_name = 'ausentismos/ausentismo_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_vendedores_abm'):
        #     return redirect(reverse('principal'))
        return super(AusentismoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        form.instance.usuario = usuario_actual(self.request)        
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

    def get_success_url(self):
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return reverse('ausentismo_listado')

    
class AusentismoEditView(VariablesMixin,UpdateView):
    form_class = AusentismoForm
    model = ausentismo
    pk_url_kwarg = 'id'
    template_name = 'ausentismos/ausentismo_form.html'
    

    @method_decorator(login_required)
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

    def get_success_url(self):        
        return reverse('ausentismo_listado')          


class AusentismoVerView(VariablesMixin,DetailView):
    model = ausentismo
    pk_url_kwarg = 'id'
    context_object_name = 'a'
    template_name = 'ausentismos/ausentismo_detalle.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(AusentismoVerView, self).dispatch(*args, **kwargs)        


# @login_required 
def ausentismo_baja_alta(request,id):
    aus = ausentismo.objects.get(pk=id)     
    aus.baja = not aus.baja
    aus.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("ausentismo_listado"))     