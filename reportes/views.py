# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from general.views import VariablesMixin,getVariablesMixin
from laboralsalud.utilidades import ultimo_anio,hoy,DecimalEncoder
from .forms import ConsultaPeriodo
from datetime import datetime,date,timedelta
from django.utils import timezone
from dateutil.relativedelta import *
from ausentismos.models import ausentismo
from django.shortcuts import render, redirect, get_object_or_404,render_to_response,HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from django.db.models import DateTimeField, ExpressionWrapper, F,DecimalField,IntegerField
import json
from decimal import Decimal
from django.db.models import Q,Sum,Count,FloatField,Func
from django.db.models.functions import Coalesce
import decimal
################################################################

def calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot):
    tasa_ausentismo = (Decimal(dias_caidos_tot) / Decimal(dias_laborables * empleados_tot))*100 
    tasa_ausentismo = Decimal(tasa_ausentismo).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP) 
    return tasa_ausentismo

class ReporteResumenPeriodo(VariablesMixin,TemplateView):
    template_name = 'reportes/resumen_periodo.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):         
        # limpiar_sesion(self.request)        
        # if not tiene_permiso(self.request,'rep_varios'):
        #     return redirect(reverse('principal'))  
        return super(ReporteResumenPeriodo, self).dispatch(*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReporteResumenPeriodo, self).get_context_data(**kwargs)

        form = ConsultaPeriodo(self.request.POST or None,request=self.request)            
        fecha = date.today()        
               
        fdesde = ultimo_anio()
        fhasta = hoy()
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     

            ausentismos = ausentismo.objects.filter(baja=False)                      
          
            if fdesde:                
                ausentismos = ausentismos.filter(Q(aus_fcrondesde__gte=fdesde,tipo_ausentismo=1)|Q(art_fcrondesde__gte=fdesde,tipo_ausentismo__gte=2))                         
            if fhasta:                
                ausentismos = ausentismos.filter(Q(aus_fcronhasta__lte=fhasta,tipo_ausentismo=1)|Q(art_fcronhasta__lte=fhasta,tipo_ausentismo__gte=2))         
            if empresa:
                ausentismos= ausentismos.filter(empleado__empresa=empresa)            
            if empleado:
                ausentismos= ausentismos.filter(empleado=empleado)

            if int(tipo_ausentismo) > 0: 
                ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))


        else:
            
            ausentismos = None            

        context['form'] = form
        context['fecha'] = fecha        
        context['fdesde'] = fdesde
        context['fhasta'] = fhasta
        context['ausentismos'] = ausentismos
        dias_laborales = 0
        dias_caidos_tot = 0
        empleados_tot = 0
        dias_trab_tot = 0
        tasa_ausentismo = 0
        aus_total = None
        aus_inc = None
        aus_acc = None
        dias_laborables = int(relativedelta(fhasta,fdesde).days)+1       
        porc_dias_trab_tot = 100

        if ausentismos:
            
            #AUSENTISMO TOTAL            
            empleados_tot = ausentismos.values('empleado').distinct().count()
            # empleados_tot = 77
            dias_caidos_tot = ausentismos.aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)+Coalesce('art_diascaidos', 0)))['dias_caidos'] or 0
            # dias_caidos_tot = 67            
            dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot
            tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)        
            porc_dias_trab_tot = 100 - tasa_ausentismo        
            
            aus_total = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
            'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot}

            #AUSENTISMO INCULPABLE
            ausentismos_inc = ausentismos.filter(tipo_ausentismo=1)
            if ausentismos_inc:
                empleados_tot = ausentismos_inc.values('empleado').distinct().count()
                # empleados_tot = 77
                dias_caidos_tot = ausentismos_inc.aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)+Coalesce('art_diascaidos', 0)))['dias_caidos'] or 0
                # dias_caidos_tot = 67            
                dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot

                tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)                                      
                porc_agudos = Decimal(74.6).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
                porc_cronicos = Decimal(25).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
                porc_dias_trab_tot = 100 - tasa_ausentismo        

                aus_inc = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
                'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot,'porc_agudos':porc_agudos,'porc_cronicos':porc_cronicos}

            #AUSENTISMO ACCIDENTES
            ausentismos_acc = ausentismos.filter(tipo_ausentismo=2)
            if ausentismos_acc:
                empleados_tot = ausentismos_acc.values('empleado').distinct().count()
                # empleados_tot = 77
                dias_caidos_tot = ausentismos_acc.aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)+Coalesce('art_diascaidos', 0)))['dias_caidos'] or 0
                # dias_caidos_tot = 67            
                dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot
                tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)                       
                porc_dias_trab_tot = 100 - tasa_ausentismo        
                
                aus_acc = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
                'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot}

        context['aus_total']=  aus_total
        context['aus_inc']=  aus_inc
        context['aus_acc']=  aus_acc
        context['dias_laborables']=  dias_laborables
        
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

