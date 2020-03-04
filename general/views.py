# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import *
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json
import urllib

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from modal.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from django.db.models import Q,Sum,Count,FloatField,Func

from .forms import TurnosForm,ConsultaTurnos,ConsultaFechasInicio,ConfiguracionForm
from .models import turnos,configuracion
from ausentismos.models import aus_patologia,aus_diagnostico,ausentismo,ausentismos_del_dia
from entidades.models import ent_empleado,ent_empresa,ent_medico_prof
from laboralsalud.utilidades import hoy,usuario_actual,empresa_actual,TIPO_AUSENCIA,empresas_habilitadas,URL_API,mobile,esAdmin
from django.contrib import messages
import locale

class VariablesMixin(object):
    def get_context_data(self, **kwargs):
        from usuarios.views import ver_permisos
        context = super(VariablesMixin, self).get_context_data(**kwargs)
        # context['ENTIDAD_ID'] = settings.ENTIDAD_ID
        # context['ENTIDAD_DIR'] = settings.ENTIDAD_DIR
        usr= self.request.user     
        try:
            context['usuario'] = usuario_actual(self.request)                        
        except:
            context['usuario'] = None         
        
        try:
            context['usr'] = usr                        
        except:
            context['usr'] = None 
       
        try:            
            context['empresa'] = empresa_actual(self.request)   
        except:
            context['empresa'] = None    
                
        try:
            context['esAdmin'] = (self.request.user.userprofile.id_usuario.tipoUsr == 0)     
        except:
            context['esAdmin'] = False             
   
        
        permisos_grupo = ver_permisos(self.request)
        context['permisos_grupo'] = permisos_grupo        
        context['permisos_empelados'] = ('aus_pantalla' in permisos_grupo)or('empl_pantalla' in permisos_grupo)or('turnos_pantalla' in permisos_grupo)
        context['permisos_indicadores'] = ('indic_pantalla' in permisos_grupo)or('indic_anual_pantalla' in permisos_grupo)
        context['permisos_configuracion'] = ('art_pantalla' in permisos_grupo)or('emp_pantalla' in permisos_grupo)or('med_pantalla' in permisos_grupo)\
                                            or('pat_pantalla' in permisos_grupo)or('diag_pantalla' in permisos_grupo)or('ptrab_pantalla' in permisos_grupo)or('esp_pantalla' in permisos_grupo)
        
        context['inicio_ausentismos'] = ('inicio_ausentismos' in permisos_grupo)or('inicio_controles' in permisos_grupo)
        context['inicio_turnos'] = ('inicio_turnos' in permisos_grupo)
        context['empresas'] = ent_empresa.objects.filter(baja=False)
        context['sitio_mobile'] = mobile(self.request)
        context['hoy'] =  hoy()
        # context['EMAIL_CONTACTO'] = EMAIL_CONTACTO                        
        return context

def getVariablesMixin(request):
    from usuarios.views import ver_permisos
    context = {}     
    usr= request.user     
    try:
        context['usuario'] = usuario_actual(request)                        
    except:
        context['usuario'] = None         
    
    try:
        context['usr'] = usr                        
    except:
        context['usr'] = None 
   
    try:            
        context['empresa'] = empresa_actual(request)   
    except:
        context['empresa'] = None    

    try:
        context['esAdmin'] = (request.user.userprofile.id_usuario.tipoUsr == 0)                        
    except:
        context['esAdmin'] = False 

    permisos_grupo = ver_permisos(request)
    context['permisos_grupo'] = permisos_grupo        
    context['permisos_empelados'] = ('aus_pantalla' in permisos_grupo)or('empl_pantalla' in permisos_grupo)or('turnos_pantalla' in permisos_grupo)
    context['permisos_indicadores'] = ('indic_pantalla' in permisos_grupo)or('indic_anual_pantalla' in permisos_grupo)
    context['permisos_configuracion'] = ('art_pantalla' in permisos_grupo)or('emp_pantalla' in permisos_grupo)or('med_pantalla' in permisos_grupo)or('med_pantalla' in permisos_grupo)\
                                        or('pat_pantalla' in permisos_grupo)or('diag_pantalla' in permisos_grupo)or('ptrab_pantalla' in permisos_grupo)or('esp_pantalla' in permisos_grupo)
    context['inicio_ausentismos'] = ('inicio_ausentismos' in permisos_grupo)or('inicio_controles' in permisos_grupo)
    context['inicio_turnos'] = ('inicio_turnos' in permisos_grupo)                                        

    context['empresas'] = ent_empresa.objects.filter(baja=False)
    context['sitio_mobile'] = mobile(request)
    context['hoy'] =  hoy()
    return context
    
class PrincipalView(VariablesMixin,TemplateView):
    template_name = 'index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PrincipalView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrincipalView, self).get_context_data(**kwargs)              
        
        form = ConsultaFechasInicio(self.request.POST or None)  
        fecha1=hoy()        
        fecha2=hoy()        
        if form.is_valid():
            fecha1 = form.cleaned_data['fecha1']
            fecha2 = form.cleaned_data['fecha2']
        if not fecha1:
            fecha1=hoy()
        if not fecha2:
            fecha2=hoy()            
           
        ausentismos = ausentismos_del_dia(self.request,fecha1).order_by('-aus_fcontrol')
        fechas_control = ausentismo.objects.filter(baja=False,aus_fcontrol=fecha1,empleado__empresa__pk__in=empresas_habilitadas(self.request)).order_by('-aus_fcontrol')
        prox_turnos = turnos.objects.filter(empresa__pk__in=empresas_habilitadas(self.request),fecha__gte=fecha2)
        
        context['form'] = form
        context['ausentismo'] = ausentismos.select_related('empleado','empleado__empresa','aus_grupop','aus_diagn')
        context['turnos'] = prox_turnos.select_related('empleado','empleado__empresa','usuario_carga')
        context['fechas_control'] = fechas_control.select_related('empleado','empleado__empresa','aus_grupop','aus_diagn')
       
        # vars_sistema = settings
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

def buscarDatosAPICUIT(request):      
   try:                            
    cuit = request.GET['cuit']
    data = urllib.urlopen(URL_API+cuit).read()    
    d = json.loads(data) 

    imp = [x['idImpuesto'] for x in d['impuesto']]    
    if (10 in imp):
        id_cat=1
    elif (11 in imp):
        id_cat=1
    elif (30 in imp):
        id_cat=1
    elif (20 in imp):
        id_cat=6
    elif (32 in imp):
        id_cat=4
    elif (33 in imp):
        id_cat=2
    else:
        id_cat=5
    d.update({'categoria': id_cat})        
   except:
    d= []
   return HttpResponse( json.dumps(d), content_type='application/json' ) 

from django.forms.models import model_to_dict

def buscarDatosEntidad(request):                     
   lista= {}
   id = request.GET['id']
   e = ent_empleado.objects.get(pk=id)   
   lista = {'id':e.id,'nro_doc':e.nro_doc,'legajo':e.legajo,'apellido_y_nombre':e.apellido_y_nombre,'fecha_nac':e.fecha_nac,
            'domicilio':e.domicilio,'provincia':e.get_provincia_display(),'localidad':e.localidad,'cod_postal':e.cod_postal,
            'email':e.email,'telefono':e.telefono,'celular':e.celular,'art':e.get_art(),'empresa':e.get_empresa(),
            'empr_fingreso':e.empr_fingreso,'trab_cargo':e.get_cargo(),'trab_fingreso':e.trab_fingreso,'trab_fbaja':e.trab_fbaja,
            'trab_armas':e.trab_armas,'trab_tareas_dif':e.trab_tareas_dif,'trab_preocupac':e.trab_preocupac,'trab_preocup_fecha':e.trab_preocup_fecha,
            'edad':e.get_edad,'antig_empresa':e.get_antiguedad_empr,'antig_trabajo':e.get_antiguedad_trab,'id_empresa':e.empresa.pk
        }
   # try:
   #    id = request.GET['id']
   #    entidad = ent_empleado.objects.get(id=id)   
   #    qs_json = serializers.serialize('json', entidad)


   # except:
   #  lista= {}
   return HttpResponse( json.dumps(lista, cls=DjangoJSONEncoder), content_type='application/json' )  


# @login_required 
def recargar_empleados(request):
    context={}
    lista = []
    empleados = ent_empleado.objects.filter(empresa__pk__in=empresas_habilitadas(request),baja=False).order_by('apellido_y_nombre')    
    for e in empleados:
        lista.append({'id':e.pk,'nombre':e.get_empleado()})
    context["empleados"]=lista
    return HttpResponse(json.dumps(context))

def recargar_empleados_empresa(request,id):
    context={}
    lista = []
    empleados = ent_empleado.objects.filter(empresa__pk=id,baja=False).order_by('apellido_y_nombre')        
    for e in empleados:
        lista.append({'id':e.pk,'nombre':e.get_empleado()})
    context["empleados"]=lista
    return HttpResponse(json.dumps(context))

def recargar_medicos(request):
    context={}
    lista = []
    medicos = ent_medico_prof.objects.filter(baja=False)   
    for e in medicos:
        lista.append({'id':e.pk,'nombre':e.get_medico()})
    context["medicos"]=lista
    return HttpResponse(json.dumps(context))    

def recargar_diagnosticos(request):
    context={}
    lista = []
    diagnosticos = aus_diagnostico.objects.filter(baja=False)           
    for e in diagnosticos:
        lista.append({'id':e.pk,'nombre':e.diagnostico.upper()})
    context["diagnosticos"]=lista    
    return HttpResponse(json.dumps(context))    

def recargar_patologias(request):
    context={}
    lista = []
    patologias = aus_patologia.objects.filter(baja=False)   
    for e in patologias:
        lista.append({'id':e.pk,'nombre':e.get_patologia()})
    context["patologias"]=lista
    return HttpResponse(json.dumps(context))        



############ TURNOS ############################
from .calendario import Calendar
from django.utils.safestring import mark_safe
from usuarios.views import tiene_permiso

class TurnosView(VariablesMixin,ListView):
    model = turnos
    template_name = 'general/turnos_listado.html'
    context_object_name = 'turnos'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs): 
    #     if not tiene_permiso(self.request,'turnos_pantalla'):
    #         return redirect(reverse('principal'))
    #     return super(TurnosView, self).dispatch(*args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super(TurnosView, self).get_context_data(**kwargs)
        form = ConsultaTurnos(self.request.POST or None,request=self.request)   
        listado = turnos.objects.filter(empresa__pk__in=empresas_habilitadas(self.request))
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['qempresa']                           
            empleado= form.cleaned_data['qempleado']                           
            estado = form.cleaned_data['qestado']

            listado = turnos.objects.filter(empresa__pk__in=empresas_habilitadas(self.request))
           
            if fdesde:                
                listado = listado.filter(fecha__gte=fdesde)                         
            if fhasta:                
                listado = listado.filter(fecha__lte=fhasta)                         
            if empresa:
                listado= listado.filter(empresa=empresa)            
            if empleado:
                listado= listado.filter(Q(empleado__apellido_y_nombre__icontains=empleado)|Q(empleado__nro_doc__icontains=empleado))

            if int(estado)<3:
                listado= listado.filter(estado=estado)            
                
        context['form'] = form        
        context['turnos'] = listado.select_related('empleado','empresa','usuario_carga')



        return context
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
    

class TurnosCreateView(VariablesMixin,AjaxCreateView):
    form_class = TurnosForm
    template_name = 'modal/general/form_turnos.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'turnos_pantalla'):
            return redirect(reverse('principal'))
        return super(TurnosCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        form.instance.usuario_carga = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(TurnosCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TurnosCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(TurnosCreateView, self).get_initial()                       
        initial['request'] = self.request                
        initial['tipo_form'] = 'ALTA'
        return initial    

    def form_invalid(self, form):
        return super(TurnosCreateView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return reverse('turnos_listado')


class TurnosEditView(VariablesMixin,AjaxUpdateView):
    form_class = TurnosForm
    model = turnos
    pk_url_kwarg = 'id'
    template_name = 'modal/general/form_turnos.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not tiene_permiso(self.request,'turnos_pantalla'):
            return redirect(reverse('principal'))
        return super(TurnosEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(TurnosEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(TurnosEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(TurnosEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(TurnosEditView, self).get_initial()                      
        initial['tipo_form'] = 'EDICION'  
        return initial            

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)                               
        form.fields['empleado'].widget.attrs['disabled'] = True                    
        form.fields['empresa'].widget.attrs['disabled'] = 'disabled'                    
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return reverse('turnos_listado')


class TurnosVerView(VariablesMixin,DetailView):
    model = turnos
    pk_url_kwarg = 'id'
    context_object_name = 't'
    template_name = 'general/turnos_detalle.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        return super(TurnosVerView, self).dispatch(*args, **kwargs)   

@login_required 
def turno_eliminar(request,id):
    if not tiene_permiso(request,'turnos_pantalla'):
            return redirect(reverse('principal'))
    ent = turnos.objects.get(pk=id).delete()    
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("turnos_listado"))            

@login_required 
def turno_estado(request,id,estado):
    if not tiene_permiso(request,'turnos_pantalla'):
            return redirect(reverse('principal'))
    ent = turnos.objects.get(pk=id)     
    ent.estado = estado
    ent.save()       
    messages.success(request, u'¡Los datos se guardaron con éxito!')
    return HttpResponseRedirect(reverse("turnos_listado"))  


class ConfiguracionEditView(VariablesMixin,UpdateView):
    form_class = ConfiguracionForm
    model = configuracion
    pk_url_kwarg = 'id'
    template_name = 'general/configuracion_form.html'
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        if not esAdmin(self.request):
             return redirect(reverse('principal'))
        return super(ConfiguracionEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):        
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(ConfiguracionEditView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ConfiguracionEditView, self).get_form_kwargs()        
        return kwargs

    def form_invalid(self, form):         
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):    
        initial = super(ConfiguracionEditView, self).get_initial()
        return initial     