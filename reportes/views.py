# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime,date,timedelta
from django.utils import timezone
from dateutil.relativedelta import *
from django.shortcuts import render, redirect, get_object_or_404,render_to_response,HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from django.db.models import DateTimeField, ExpressionWrapper, F,DecimalField,IntegerField
import json
from decimal import Decimal
from django.db.models import Q,Sum,Count,FloatField,Func
from django.db.models.functions import Coalesce
import decimal

from general.views import VariablesMixin,getVariablesMixin
from laboralsalud.utilidades import ultimo_anio,hoy,DecimalEncoder,MESES
from .forms import ConsultaPeriodo,ConsultaAnual
from ausentismos.models import ausentismo
from usuarios.views import tiene_permiso
################################################################

def calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot):
    tasa_ausentismo = (Decimal(dias_caidos_tot) / Decimal(dias_laborables * empleados_tot))*100 
    tasa_ausentismo = Decimal(tasa_ausentismo).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP) 
    return tasa_ausentismo

class ReporteResumenPeriodo(VariablesMixin,TemplateView):
    template_name = 'reportes/resumen_periodo.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                 
        if not tiene_permiso(self.request,'indic_pantalla'):
            return redirect(reverse('principal'))  
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
            trab_cargo= form.cleaned_data['trab_cargo']                           

            ausentismos = ausentismo.objects.filter(baja=False)                      
          
            if fdesde:                
                ausentismos = ausentismos.filter(Q(aus_fcrondesde__gte=fdesde,tipo_ausentismo=1)|Q(art_fcrondesde__gte=fdesde,tipo_ausentismo__gte=2))                         
            if fhasta:                
                ausentismos = ausentismos.filter(Q(aus_fcronhasta__lte=fhasta,tipo_ausentismo=1)|Q(art_fcronhasta__lte=fhasta,tipo_ausentismo__gte=2))         
            if empresa:
                ausentismos= ausentismos.filter(empleado__empresa=empresa)            
            if empleado:
                ausentismos= ausentismos.filter(Q(empleado__apellido_y_nombre__icontains=empleado)|Q(empleado__nro_doc__icontains=empleado))
            if trab_cargo:
                ausentismos= ausentismos.filter(empleado__trab_cargo=trab_cargo)            

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
        dias_laborables = int((fhasta-fdesde).days+1)   
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
            #F('college_start_date') - F('school_passout_date')
            #AUSENTISMO INCULPABLE
            ausentismos_inc = ausentismos.filter(tipo_ausentismo=1)
            if ausentismos_inc:
                empleados_tot = ausentismos_inc.values('empleado').distinct().count()
                # empleados_tot = 77
                dias_caidos_tot = ausentismos_inc.aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)+Coalesce('art_diascaidos', 0)))['dias_caidos'] or 0
                # dias_caidos_tot = 67            
                dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot

                tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)                                      
                
                agudos = ausentismos_inc.filter(Q(aus_diascaidos__lte=30)|Q(art_diascaidos__lte=30)).aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)+Coalesce('art_diascaidos', 0)))['dias_caidos'] or 0
                graves = ausentismos_inc.filter(Q(aus_diascaidos__gt=30)|Q(art_diascaidos__gt=30)).aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)+Coalesce('art_diascaidos', 0)))['dias_caidos'] or 0
                
                
                porc_agudos = (Decimal(agudos) / Decimal(dias_caidos_tot))*100 
                porc_cronicos = (Decimal(graves) / Decimal(dias_caidos_tot))*100 

                porc_agudos = Decimal(porc_agudos).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
                porc_cronicos = Decimal(porc_cronicos).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
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

                tot_accidentes = ausentismos_acc.count()
                
                acc_denunciados = (Decimal(ausentismos_acc.exclude(Q(art_ndenuncia__isnull=True)|Q(art_ndenuncia__exact='')).count()) / Decimal(tot_accidentes))*100 
                acc_sin_denunciar = (Decimal(ausentismos_acc.filter(Q(art_ndenuncia__isnull=True)|Q(art_ndenuncia__exact='')).count()) / Decimal(tot_accidentes))*100 
                acc_itinere = (Decimal(ausentismos_acc.filter(art_tipo_accidente=2).count()) / Decimal(tot_accidentes))*100 
                acc_trabajo = (Decimal(ausentismos_acc.filter(art_tipo_accidente=1).count()) / Decimal(tot_accidentes))*100 
                
                aus_acc = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
                'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot,'tot_accidentes':tot_accidentes,'acc_denunciados':acc_denunciados,
                'acc_sin_denunciar':acc_sin_denunciar,'acc_itinere':acc_itinere,'acc_trabajo':acc_trabajo}
                

        context['aus_total']=  aus_total
        context['aus_inc']=  aus_inc
        context['aus_acc']=  aus_acc
        context['dias_laborables']=  dias_laborables
        
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)



class ReporteResumenAnual(VariablesMixin,TemplateView):
    template_name = 'reportes/resumen_anual.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):                 
        if not tiene_permiso(self.request,'indic_pantalla'):
            return redirect(reverse('principal'))  
        return super(ReporteResumenAnual, self).dispatch(*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReporteResumenAnual, self).get_context_data(**kwargs)

        form = ConsultaAnual(self.request.POST or None,request=self.request)            
        fecha = date.today()        
               
        fdesde = ultimo_anio()
        fhasta = hoy()
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     
            trab_cargo= form.cleaned_data['trab_cargo']                           

            ausentismos = ausentismo.objects.filter(baja=False)                      
          
            if fdesde:                
                ausentismos = ausentismos.filter(Q(aus_fcrondesde__gte=fdesde,tipo_ausentismo=1)|Q(art_fcrondesde__gte=fdesde,tipo_ausentismo__gte=2))                         
            if fhasta:                
                ausentismos = ausentismos.filter(Q(aus_fcronhasta__lte=fhasta,tipo_ausentismo=1)|Q(art_fcronhasta__lte=fhasta,tipo_ausentismo__gte=2))         
            if empresa:
                ausentismos= ausentismos.filter(empleado__empresa=empresa)            
            if empleado:
                ausentismos= ausentismos.filter(Q(empleado__apellido_y_nombre__icontains=empleado)|Q(empleado__nro_doc__icontains=empleado))
            if trab_cargo:
                ausentismos= ausentismos.filter(empleado__trab_cargo=trab_cargo)            

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
        dias_laborables = int((fhasta-fdesde).days+1)   
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
            #F('college_start_date') - F('school_passout_date')
            
                

        context['aus_total']=  aus_total       
        context['dias_laborables']=  dias_laborables
        meses = list()
        import locale        
        locale.setlocale(locale.LC_ALL, '')
        for m in MESES:                        
                meses.append(m[0])
        context['meses']=  meses       
        
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

