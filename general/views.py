# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import *
from django.shortcuts import render
from laboralsalud.utilidades import URL_API
from django.core.serializers.json import DjangoJSONEncoder
import json
import urllib
from django.views.generic import TemplateView
from entidades.models import ent_empleado

class VariablesMixin(object):
    def get_context_data(self, **kwargs):
        context = super(VariablesMixin, self).get_context_data(**kwargs)
        # context['ENTIDAD_ID'] = settings.ENTIDAD_ID
        # context['ENTIDAD_DIR'] = settings.ENTIDAD_DIR
        # usr= self.request.user     
        # try:
        #     context['usuario'] = usuario_actual(self.request)                        
        # except:
        #     context['usuario'] = None         

        # try:
        #     context['usr'] = usr                        
        # except:
        #     context['usr'] = None 

        # try:
        #     empresa = empresa_actual(self.request)
        # except gral_empresa.DoesNotExist:
        #     empresa = None
                      
        # context['empresa'] = empresa           
        # context['settings'] = settings 
        
        # try:
        #     tipo_usr = usr.userprofile.id_usuario.tipoUsr
        #     context['tipo_usr'] = tipo_usr
        #     context['habilitado_contador'] = habilitado_contador(tipo_usr)
        # except:
        #     context['tipo_usr'] = 1
        #     context['habilitado_contador'] = False

        # permisos_grupo = ver_permisos(self.request)
        # context['permisos_grupo'] = permisos_grupo        
        # context['permisos_ingresos'] = ('cpb_ventas' in permisos_grupo)or('cpb_cobranzas' in permisos_grupo)or('cpb_remitos' in permisos_grupo)or('cpb_presupuestos' in permisos_grupo)or('cpb_liqprod_abm' in permisos_grupo)        
        # context['permisos_egresos'] = ('cpb_compras' in permisos_grupo)or('cpb_pagos' in permisos_grupo)or('cpb_movimientos' in permisos_grupo)        
        # context['permisos_trabajos'] = ('trab_pedidos' in permisos_grupo)or('trab_trabajos' in permisos_grupo)or('trab_colocacion' in permisos_grupo)
        # context['permisos_rep_ingr_egr'] = ('rep_cta_cte_clientes' in permisos_grupo)or('rep_saldos_clientes' in permisos_grupo)or('rep_cta_cte_prov' in permisos_grupo)or('rep_saldos_prov' in permisos_grupo)or('rep_varios' in permisos_grupo)
        # context['permisos_rep_contables'] = ('rep_libro_iva' in permisos_grupo)or('rep_libro_iva' in permisos_grupo)        
        # context['permisos_entidades'] = ('ent_clientes' in permisos_grupo)or('ent_proveedores' in permisos_grupo)or('ent_vendedores' in permisos_grupo)        
        # context['permisos_productos'] = ('prod_productos' in permisos_grupo)or('prod_productos_abm' in permisos_grupo)
        # context['permisos_rep_finanzas'] = ('rep_caja_diaria' in permisos_grupo)or('rep_seguim_cheques' in permisos_grupo)or('rep_saldos_cuentas' in permisos_grupo)
        # context['homologacion'] = empresa.homologacion
        # context['sitio_mobile'] = mobile(self.request)
        # context['hoy'] =  hoy()
        # context['EMAIL_CONTACTO'] = EMAIL_CONTACTO                        
        return context

class PrincipalView(VariablesMixin,TemplateView):
    template_name = 'base.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PrincipalView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrincipalView, self).get_context_data(**kwargs)              
        # vars_sistema = settings
        return context




# @login_required 
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
            'edad':e.get_edad,'antig_empresa':e.get_antiguedad_empr,'antig_trabajo':e.get_antiguedad_trab
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
    empleados = ent_empleado.objects.filter(baja=False).order_by('apellido_y_nombre')    
    for e in empleados:
        lista.append({'id':e.pk,'nombre':e.get_empleado()})
    context["empleados"]=lista
    print lista
    return HttpResponse(json.dumps(context))

