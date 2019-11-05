# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import *
from django.shortcuts import render
from laboralsalud.utilidades import URL_API
from django.core.serializers.json import DjangoJSONEncoder
import json
import urllib
from ausentismos.models import aus_patologia,aus_diagnostico,ausentismo
from entidades.models import ent_empleado,ent_empresa,ent_medico_prof
from laboralsalud.utilidades import hoy,usuario_actual,empresa_actual
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from fm.views import AjaxCreateView,AjaxUpdateView,AjaxDeleteView
from .forms import TurnosForm
from .models import turnos

class VariablesMixin(object):
    def get_context_data(self, **kwargs):
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

        context['esAdmin'] = (self.request.user.userprofile.id_usuario.tipoUsr == 0)     
        try:
            context['esAdmin'] = (self.request.user.userprofile.id_usuario.tipoUsr == 0)                        
        except:
            context['esAdmin'] = False 
   
        context['empresas'] = ent_empresa.objects.filter(baja=False)
        # context['sitio_mobile'] = mobile(self.request)
        context['hoy'] =  hoy()
        # context['EMAIL_CONTACTO'] = EMAIL_CONTACTO                        
        return context

def getVariablesMixin(request):
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

    context['empresas'] = ent_empresa.objects.filter(baja=False)
    # context['sitio_mobile'] = mobile(self.request)
    context['hoy'] =  hoy()
    return context
    
class PrincipalView(VariablesMixin,TemplateView):
    template_name = 'index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PrincipalView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrincipalView, self).get_context_data(**kwargs)              

        context['ausentismo'] = ausentismo.objects.filter(baja=False)[:20]


        # vars_sistema = settings
        return context

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
        lista.append({'id':e.pk,'nombre':e.get_diagnostico()})
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
           
class TurnosView(VariablesMixin,ListView):
    model = turnos
    template_name = 'turnos/turnos_listado.html'
    context_object_name = 'turnos'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes'):
        #     return redirect(reverse('principal'))
        return super(TurnosView, self).dispatch(*args, **kwargs)    

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
    

class TurnosCreateView(VariablesMixin,AjaxCreateView):
    form_class = TurnosForm
    template_name = 'fm/general/form_turnos.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_vendedores_abm'):
        #     return redirect(reverse('principal'))
        return super(TurnosCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):                
        #form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, u'Los datos se guardaron con éxito!')
        return super(TurnosCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TurnosCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs  

    def get_initial(self):    
        initial = super(TurnosCreateView, self).get_initial()                       
        initial['request'] = self.request        
        return initial    

    def form_invalid(self, form):
        return super(TurnosCreateView, self).form_invalid(form)


class TurnosEditView(VariablesMixin,AjaxUpdateView):
    form_class = TurnosForm
    model = turnos
    pk_url_kwarg = 'id'
    template_name = 'fm/general/form_turnos.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): 
        # if not tiene_permiso(self.request,'ent_clientes_abm'):
        #     return redirect(reverse('principal'))
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
        initial = super(EmpresaEditView, self).get_initial()                      
        initial['tipo_form'] = 'EDICION'  
        return initial            


# class EmpresaVerView(VariablesMixin,DetailView):
#     model = ent_empresa
#     pk_url_kwarg = 'id'
#     context_object_name = 'empresa'
#     template_name = 'entidades/empresa_detalle.html'

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs): 
#         return super(EmpresaVerView, self).dispatch(*args, **kwargs)        


# @login_required 
# def empresa_baja_alta(request,id):
#     ent = ent_empresa.objects.get(pk=id)     
#     ent.baja = not ent.baja
#     ent.save()       
#     messages.success(request, u'¡Los datos se guardaron con éxito!')
#     return HttpResponseRedirect(reverse("empresa_listado"))            
