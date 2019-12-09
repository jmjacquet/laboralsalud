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
from .forms import ARTForm,CargoForm,EspecialidadForm,MedProfForm,EmpresaForm,EmpleadoForm,ConsultaEmpleados
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId,usuario_actual,empresa_actual,empresas_habilitadas
from django.contrib.auth.decorators import login_required
from usuarios.views import tiene_permiso
from django.utils.decorators import method_decorator
############ ART ############################

class ARTView(VariablesMixin,ListView):
    model = ent_art
    template_name = 'entidades/art_listado.html'
    context_object_name = 'art'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'art_pantalla'):
            return redirect(reverse('principal'))
        return super(ARTView, self).dispatch(*args, **kwargs)
    

class ARTCreateView(VariablesMixin,AjaxCreateView):
    form_class = ARTForm
    template_name = 'fm/entidades/form_art.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'art_pantalla'):
            return redirect(reverse('principal'))
        return super(ARTCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        form.instance.usuario = usuario_actual(self.request)
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
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'art_pantalla'):
            return redirect(reverse('principal'))
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(ARTVerView, self).dispatch(*args, **kwargs)        


@login_required 
def art_baja_alta(request,id):
    if not tiene_permiso(request,'art_pantalla'):
            return redirect(reverse('principal'))
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'ptrab_pantalla'):
            return redirect(reverse('principal'))
        return super(CargoView, self).dispatch(*args, **kwargs)
    

class CargoCreateView(VariablesMixin,AjaxCreateView):
    form_class = CargoForm
    template_name = 'fm/entidades/form_cargo.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'ptrab_pantalla'):
            return redirect(reverse('principal'))
        return super(CargoCreateView, self).dispatch(*args, **kwargs)

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
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'ptrab_pantalla'):
            return redirect(reverse('principal'))
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(CargoVerView, self).dispatch(*args, **kwargs)        


@login_required 
def cargo_baja_alta(request,id):
    if not tiene_permiso(request,'ptrab_pantalla'):
            return redirect(reverse('principal'))
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'esp_pantalla'):
            return redirect(reverse('principal'))
        return super(EspecialidadView, self).dispatch(*args, **kwargs)
    

class EspecialidadCreateView(VariablesMixin,AjaxCreateView):
    form_class = EspecialidadForm
    template_name = 'fm/entidades/form_esp.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'esp_pantalla'):
            return redirect(reverse('principal'))
        return super(EspecialidadCreateView, self).dispatch(*args, **kwargs)

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
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'esp_pantalla'):
            return redirect(reverse('principal'))
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(EspecialidadVerView, self).dispatch(*args, **kwargs)        


@login_required 
def especialidad_baja_alta(request,id):
    if not tiene_permiso(request,'esp_pantalla'):
            return redirect(reverse('principal'))
    ent = ent_especialidad.objects.get(pk=id)     
    ent.baja = not ent.baja
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("especialidad_listado"))        



############ MEDICO / PROFESIONAL ############################

class MedProfView(VariablesMixin,ListView):
    model = ent_medico_prof
    template_name = 'entidades/med_prof_listado.html'
    context_object_name = 'med'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'med_pantalla'):
            return redirect(reverse('principal'))
        return super(MedProfView, self).dispatch(*args, **kwargs)
    

class MedProfCreateView(VariablesMixin,AjaxCreateView):
    form_class = MedProfForm
    template_name = 'fm/entidades/form_med_prof.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'med_pantalla'):
            return redirect(reverse('principal'))
        return super(MedProfCreateView, self).dispatch(*args, **kwargs)

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
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'med_pantalla'):
            return redirect(reverse('principal'))
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(MedProfVerView, self).dispatch(*args, **kwargs)        


@login_required 
def medico_prof_baja_alta(request,id):
    if not tiene_permiso(request,'med_pantalla'):
            return redirect(reverse('principal'))
    ent = ent_medico_prof.objects.get(pk=id)     
    ent.baja = not ent.baja
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("medico_prof_listado"))        



############ EMPRESAS ############################
           
class EmpresaView(VariablesMixin,ListView):
    model = ent_empresa
    template_name = 'entidades/empresa_listado.html'
    context_object_name = 'empresas'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'emp_pantalla'):
            return redirect(reverse('principal'))
        return super(EmpresaView, self).dispatch(*args, **kwargs)    

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
    

class EmpresaCreateView(VariablesMixin,AjaxCreateView):
    form_class = EmpresaForm
    template_name = 'fm/entidades/form_empresa.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'emp_pantalla'):
            return redirect(reverse('principal'))
        return super(EmpresaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(EmpresaCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpresaCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(EmpresaCreateView, self).get_initial()               
        initial['codigo'] = '{0:0{width}}'.format((ultimoNroId(ent_empresa)+1),width=4)
        initial['request'] = self.request        
        initial['tipo_form'] = 'ALTA'  
        return initial    

    def form_invalid(self, form):
        return super(EmpresaCreateView, self).form_invalid(form)


class EmpresaEditView(VariablesMixin,AjaxUpdateView):
    form_class = EmpresaForm
    model = ent_empresa
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_empresa.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'emp_pantalla'):
            return redirect(reverse('principal'))
        return super(EmpresaEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(EmpresaEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EmpresaEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpresaEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(EmpresaEditView, self).get_initial()                      
        initial['tipo_form'] = 'EDICION'  
        return initial            


class EmpresaVerView(VariablesMixin,DetailView):
    model = ent_empresa
    pk_url_kwarg = 'id'
    context_object_name = 'empresa'
    template_name = 'entidades/empresa_detalle.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(EmpresaVerView, self).dispatch(*args, **kwargs)        


@login_required 
def empresa_baja_alta(request,id):
    if not tiene_permiso(request,'emp_pantalla'):
            return redirect(reverse('principal'))
    ent = ent_empresa.objects.get(pk=id)     
    ent.baja = not ent.baja
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("empresa_listado"))            


############ EMPLEADOS ############################

class EmpleadoView(VariablesMixin,ListView):
    model = ent_empleado
    template_name = 'entidades/empleado_listado.html'
    context_object_name = 'empleados'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'empl_pantalla'):
            return redirect(reverse('principal'))
        return super(EmpleadoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmpleadoView, self).get_context_data(**kwargs)
        form = ConsultaEmpleados(self.request.POST or None,request=self.request)   
        empleados = ent_empleado.objects.filter(empresa__pk__in=empresas_habilitadas(self.request)).select_related('empresa','trab_cargo','art')[:1000]         
        if form.is_valid():                                                        
            empresa = form.cleaned_data['empresa']                                       
            estado = form.cleaned_data['estado']
            art = form.cleaned_data['art']
            empleados = ent_empleado.objects.filter(empresa__pk__in=empresas_habilitadas(self.request)).select_related('empresa','trab_cargo','art')

                          
          
            if int(estado) == 0:  
                empleados = empleados.filter(baja=False)
            if empresa:
                empleados= empleados.filter(empresa=empresa)                        
            if art:
                empleados= empleados.filter(art=art) 
                
        context['form'] = form

        context['empleados'] = empleados



        return context
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
    

class EmpleadoCreateView(VariablesMixin,AjaxCreateView):
    form_class = EmpleadoForm
    template_name = 'fm/entidades/form_empleado.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'empl_pantalla'):
            return redirect(reverse('principal'))
        return super(EmpleadoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(EmpleadoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpleadoCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(EmpleadoCreateView, self).get_initial()               
        initial['legajo'] = '{0:0{width}}'.format((ultimoNroId(ent_empleado)+1),width=4)
        initial['request'] = self.request        
        empresa = empresa_actual(self.request)
        initial['empresa'] = empresa_actual(self.request)       
        if empresa:
            initial['art'] = empresa_actual(self.request).art  
        initial['tipo_form'] = 'ALTA'  
        return initial    

    def form_invalid(self, form):
        return super(EmpleadoCreateView, self).form_invalid(form)


class EmpleadoEditView(VariablesMixin,AjaxUpdateView):
    form_class = EmpleadoForm
    model = ent_empleado
    pk_url_kwarg = 'id'
    template_name = 'fm/entidades/form_empleado.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'empl_pantalla'):
            return redirect(reverse('principal'))
        return super(EmpleadoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(EmpleadoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EmpleadoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpleadoEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(EmpleadoEditView, self).get_initial()                      
        initial['tipo_form'] = 'EDICION'  
        return initial            


class EmpleadoVerView(VariablesMixin,DetailView):
    model = ent_empleado
    pk_url_kwarg = 'id'
    context_object_name = 'empleados'
    template_name = 'entidades/empleado_detalle.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(EmpleadoVerView, self).dispatch(*args, **kwargs)        


@login_required 
def empleado_baja_alta(request,id):
    if not tiene_permiso(request,'empl_pantalla'):
            return redirect(reverse('principal'))
    ent = ent_empleado.objects.get(pk=id)     
    ent.baja = not ent.baja
    if ent.baja:
        ent.trab_fbaja=hoy()
    else:
        ent.trab_fbaja=None
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("empleado_listado"))   


import csv, io
   

def simple_upload(request):
    data = {}    
   
    if request.method == 'POST':  
        csv_file = request.FILES["cargos"]
        #tabla = request.POST['username']     
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("simple_upload"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("simple_upload"))

        file_data = csv_file.read().decode("utf8", "ignore")

        lines = file_data.split("\n")
        cant = len(lines)
        try:
            for index,line in enumerate(lines):                      
                campos = line.split(";")
                dni = campos[0]                
                try:
                    empl = ent_empleado.objects.get(nro_doc=dni.strip())                     
                except:                    
                    legajo = campos[1]                
                    nombre = campos[2]+' '+campos[3]                
                    fecha_nac = datetime.datetime.strptime(campos[4], "%d/%m/%Y").date()                
                    art = campos[5]                
                    art = ent_art.objects.get(nombre=art.strip())         
                    empresa = campos[6]                
                    empresa = ent_empresa.objects.get(razon_social=empresa.strip())
                    puesto = campos[7]                
                    puesto = ent_cargo.objects.get(cargo=puesto.strip())                    
                    try:
                       ent_empleado.objects.update_or_create(nro_doc=dni,legajo=legajo,apellido_y_nombre=nombre,fecha_nac=fecha_nac,art=art,empresa=empresa,trab_cargo=puesto)                                          
                       print index
                    except Exception as e:
                        print e
                        print nombre                    
                    
        except Exception as e:
            print e
            print nombre

    return render(request, 'entidades/import.html')