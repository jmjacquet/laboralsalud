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
from .forms import ARTForm,CargoForm,EspecialidadForm,MedProfForm
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId


############ ART ############################

class ARTView(VariablesMixin,ListView):
    model = ent_art
    template_name = 'entidades/art_listado.html'
    context_object_name = 'art'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_clientes'):
    #         return redirect(reverse('principal'))
    #     return super(ARTView, self).dispatch(*args, **kwargs)
    

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
        initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(ent_art)+1),width=4)
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(ARTCreateView, self).form_invalid(form)


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


############ CARGO ############################

class CargoView(VariablesMixin,ListView):
    model = ent_cargo
    template_name = 'entidades/cargo_listado.html'
    context_object_name = 'cargo'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_clientes'):
    #         return redirect(reverse('principal'))
    #     return super(ARTView, self).dispatch(*args, **kwargs)
    

class CargoCreateView(VariablesMixin,AjaxCreateView):
    form_class = CargoForm
    template_name = 'fm/entidades/form_cargo.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_vendedores_abm'):
    #         return redirect(reverse('principal'))
    #     return super(ARTCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(CargoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CargoCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(CargoCreateView, self).get_initial()               
        initial['codigo'] = '{0:0{width}}'.format((ultimoNroId(ent_cargo)+1),width=4)
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(CargoCreateView, self).form_invalid(form)


class CargoEditView(VariablesMixin,AjaxUpdateView):
    form_class = CargoForm
    model = ent_cargo
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_cargo.html'
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(CargoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(CargoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CargoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(CargoEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(CargoEditView, self).get_initial()                      
        return initial            


class CargoVerView(VariablesMixin,DetailView):
    model = ent_cargo
    pk_url_kwarg = 'id'
    context_object_name = 'cargo'
    template_name = 'entidades/cargo_detalle.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     return super(VendedoresVerView, self).dispatch(*args, **kwargs)        


# @login_required 
def cargo_baja_alta(request,id):
    ent = ent_cargo.objects.get(pk=id)     
    ent.baja = not ent.baja
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("cargo_listado"))    


############ ESPECIALIDAD ############################

class EspecialidadView(VariablesMixin,ListView):
    model = ent_especialidad
    template_name = 'entidades/especialidad_listado.html'
    context_object_name = 'esp'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_clientes'):
    #         return redirect(reverse('principal'))
    #     return super(ARTView, self).dispatch(*args, **kwargs)
    

class EspecialidadCreateView(VariablesMixin,AjaxCreateView):
    form_class = EspecialidadForm
    template_name = 'fm/entidades/form_esp.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_vendedores_abm'):
    #         return redirect(reverse('principal'))
    #     return super(ARTCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(EspecialidadCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EspecialidadCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(EspecialidadCreateView, self).get_initial()               
        initial['codigo'] = '{0:0{width}}'.format((ultimoNroId(ent_especialidad)+1),width=4)
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(EspecialidadCreateView, self).form_invalid(form)


class EspecialidadEditView(VariablesMixin,AjaxUpdateView):
    form_class = EspecialidadForm
    model = ent_especialidad
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_esp.html'
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(EspecialidadEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(EspecialidadEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EspecialidadEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(EspecialidadEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(EspecialidadEditView, self).get_initial()                      
        return initial            


class EspecialidadVerView(VariablesMixin,DetailView):
    model = ent_especialidad
    pk_url_kwarg = 'id'
    context_object_name = 'esp'
    template_name = 'entidades/especialidad_detalle.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     return super(VendedoresVerView, self).dispatch(*args, **kwargs)        


# @login_required 
def especialidad_baja_alta(request,id):
    ent = ent_especialidad.objects.get(pk=id)     
    ent.baja = not ent.baja
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("especialidad_listado"))        



############ MEDICO / PROFESIONAL ############################

class MedProfView(VariablesMixin,ListView):
    model = ent_cargo
    template_name = 'entidades/cargo_listado.html'
    context_object_name = 'cargo'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_clientes'):
    #         return redirect(reverse('principal'))
    #     return super(ARTView, self).dispatch(*args, **kwargs)
    

class MedProfCreateView(VariablesMixin,AjaxCreateView):
    form_class = MedProfForm
    template_name = 'fm/entidades/form_med_prof.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'ent_vendedores_abm'):
    #         return redirect(reverse('principal'))
    #     return super(ARTCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(MedProfCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MedProfCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(MedProfCreateView, self).get_initial()               
        initial['codigo'] = '{0:0{width}}'.format((ultimoNroId(ent_medico_prof)+1),width=4)
        initial['request'] = self.request        
        initial['tipo_form'] = 'ALTA'  
        return initial    

    def form_invalid(self, form):
        return super(MedProfCreateView, self).form_invalid(form)


class MedProfEditView(VariablesMixin,AjaxUpdateView):
    form_class = MedProfForm
    model = ent_medico_prof
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_med_prof.html'
    

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
        return super(MedProfEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(MedProfEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MedProfEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(MedProfEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(MedProfEditView, self).get_initial()                      
        initial['tipo_form'] = 'EDICION'  
        return initial            


class MedProfVerView(VariablesMixin,DetailView):
    model = ent_medico_prof
    pk_url_kwarg = 'id'
    context_object_name = 'mp'
    template_name = 'entidades/medico_prof_detalle.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     return super(VendedoresVerView, self).dispatch(*args, **kwargs)        


# @login_required 
def medico_prof_baja_alta(request,id):
    ent = ent_medico_prof.objects.get(pk=id)     
    ent.baja = not ent.baja
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("medico_prof_listado"))        