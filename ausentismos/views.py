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
from .forms import AusentismoForm,PatologiaForm,DiagnosticoForm,ConsultaAusentismos
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId,usuario_actual
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView

############ PATOLOGIAS ############################

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


############ DIAGNOSTICOS ############################

class DiagnosticoView(VariablesMixin,ListView):
    model = aus_diagnostico
    template_name = 'ausentismos/diagnostico_listado.html'
    context_object_name = 'diagnosticos'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(DiagnosticoView, self).dispatch(*args, **kwargs)
    

class DiagnosticoCreateView(VariablesMixin,AjaxCreateView):
    form_class = DiagnosticoForm
    template_name = 'fm/entidades/form_diagnostico.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_vendedores_abm'):
        #     return redirect(reverse('principal'))
        return super(DiagnosticoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(DiagnosticoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(DiagnosticoCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(DiagnosticoCreateView, self).get_initial()               
        # initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(aus_patologia)+1),width=4)
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(DiagnosticoCreateView, self).form_invalid(form)


class DiagnosticoEditView(VariablesMixin,AjaxUpdateView):
    form_class = DiagnosticoForm
    model = aus_diagnostico
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_diagnostico.html'
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(DiagnosticoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(DiagnosticoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(DiagnosticoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DiagnosticoEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(DiagnosticoEditView, self).get_initial()                      
        return initial            


############ AUSENTISMOS ############################

class AusentismoView(VariablesMixin,ListView):
    model = ausentismo
    template_name = 'ausentismos/ausentismo_listado.html'
    context_object_name = 'ausentismos'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(AusentismoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AusentismoView, self).get_context_data(**kwargs)

        form = ConsultaAusentismos(self.request.POST or None,request=self.request)   
        ausentismos = None            
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     

            ausentismos = ausentismo.objects.filter(baja=False)                      
          
            if fdesde:                
                ausentismos = ausentismos.filter(fecha_creacion__gte=fdesde)                         
            if fhasta:                
                ausentismos = ausentismos.filter(fecha_creacion__lte=fhasta)                         
            if empresa:
                ausentismos= ausentismos.filter(empleado__empresa=empresa)            
            if empleado:
                ausentismos= ausentismos.filter(empleado__apellido_y_nombre__icontains=empleado)
            if int(tipo_ausentismo) > 0: 
                ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))
                
        context['form'] = form
        context['ausentismos'] = ausentismos
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

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
        initial['tipo_form'] = 'ALTA'
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
        initial['tipo_form'] = 'EDICION'
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