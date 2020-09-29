# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime,date,timedelta
from django.utils import timezone
from django.contrib import messages
from dateutil.relativedelta import *
from django.shortcuts import render, redirect, get_object_or_404,render_to_response,HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,FormView,DetailView
from django.db.models import DateTimeField, ExpressionWrapper, F,DecimalField,IntegerField
import json
from decimal import Decimal
from django.db.models import Q,Sum,Count,FloatField,Func,Avg
from django.db.models.functions import Coalesce
import decimal
from easy_pdf.rendering import render_to_pdf_response,render_to_pdf 

from general.views import VariablesMixin,getVariablesMixin
from laboralsalud.utilidades import ultimo_anio,hoy,DecimalEncoder,MESES
from .forms import ConsultaPeriodo,ConsultaAnual
from ausentismos.models import ausentismo
from usuarios.views import tiene_permiso
from general.models import configuracion
################################################################

def calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot):
    if empleados_tot>0:
        tasa_ausentismo = (Decimal(dias_caidos_tot) / Decimal(dias_laborables * empleados_tot))*100 
        tasa_ausentismo = Decimal(tasa_ausentismo).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP) 
    else:
        return 0
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
        empresa = None
        filtro = u""
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     
            trab_cargo= form.cleaned_data['trab_cargo']                           

            ausentismos = ausentismo.objects.filter(baja=False)                      
            filtro = u"Fecha Desde: %s - Fecha Hasta: %s" % (fdesde.strftime("%d/%m/%Y"),fhasta.strftime("%d/%m/%Y"))

            if empresa:
                if empresa.casa_central:
                    ausentismos= ausentismos.filter(empleado__empresa=empresa)
                else:
                    ausentismos= ausentismos.filter(Q(empleado__empresa=empresa)|Q(empleado__empresa__casa_central=empresa))
            else:
                ausentismos= ausentismos.filter(empleado__empresa__pk__in=empresas_habilitadas(self.request))

            if empleado:
                ausentismos= ausentismos.filter(Q(empleado__apellido_y_nombre__icontains=empleado)|Q(empleado__nro_doc__icontains=empleado))
                filtro = filtro+u" - Empleado: %s" % (empleado)
            if trab_cargo:
                ausentismos= ausentismos.filter(empleado__trab_cargo=trab_cargo)            
                filtro = filtro+u" - Puesto de Trabajo: %s" % (trab_cargo)

            if int(tipo_ausentismo) > 0: 
                ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))

            ausentismos = ausentismos.filter(Q(aus_fcrondesde__range=[fdesde,fhasta])|Q(aus_fcronhasta__range=[fdesde,fhasta])
                |Q(aus_fcrondesde__lt=fdesde,aus_fcronhasta__gt=fhasta))  

        else:
            ausentismos = None            

        context['form'] = form
        context['fecha'] = fecha        
        context['fdesde'] = fdesde
        context['fhasta'] = fhasta
        context['ausentismos'] = ausentismos
        context['empresa'] = empresa
        context['titulo_reporte'] = u"REPORTE INDICADORES: %s "%(empresa)
                  
        context['filtro'] = filtro
        context['pie_pagina'] = "Sistemas Laboral Salud - %s" % (fecha.strftime("%d/%m/%Y"))
        dias_laborales = 0
        dias_caidos_tot = 0
        empleados_tot = 0
        dias_trab_tot = 0
        tasa_ausentismo = 0
        aus_total = None
        aus_inc = None
        aus_acc = None
        aus_x_grupop = None 
        max_grupop = 0
        dias_laborables = int((fhasta-fdesde).days+1)   
        empl_mas_faltadores = []
        porc_dias_trab_tot = 100
        if empresa:
            empleados_tot = empresa.cantidad_empleados()
        if ausentismos:
            
            #AUSENTISMO TOTAL            
            #empleados_tot = ausentismos.values('empleado').distinct().count()            
            
            # dias_caidos_tot = ausentismos.aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)))['dias_caidos'] or 0            
            dias_caidos_tot=dias_ausentes(fdesde,fhasta,ausentismos)               
            dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot
            tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)        
            porc_dias_trab_tot = 100 - tasa_ausentismo        
            
            ta_cant_empls = ausentismos.values('empleado').distinct().count()
            tp_cant_empls = empleados_tot- ta_cant_empls

            aus_total = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
            'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot, 'ta_cant_empls':ta_cant_empls,'tp_cant_empls':tp_cant_empls}
            
            #F('college_start_date') - F('school_passout_date')
            #AUSENTISMO INCULPABLE
            ausentismos_inc = ausentismos.filter(tipo_ausentismo=1)
            if ausentismos_inc:
                empleados_inc = ausentismos_inc.values('empleado').distinct().count()
                # empleados_tot = 77
                totales = tot_ausentes_inc(fdesde,fhasta,ausentismos_inc)
                dias_caidos_tot=totales[0] 
                # dias_caidos_tot = 67            
                dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot

                tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)                                      
                
                # agudos = ausentismos_inc.filter(aus_diascaidos__lte=30).aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)))['dias_caidos'] or 0
                # graves = ausentismos_inc.filter(aus_diascaidos__gt=30).aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)))['dias_caidos'] or 0
                agudos=totales[1] 
                graves=totales[2]                 
                
                porc_agudos = (Decimal(agudos) / Decimal(dias_caidos_tot))*100 
                porc_cronicos = (Decimal(graves) / Decimal(dias_caidos_tot))*100 

                tot_agudos = int(porc_agudos*Decimal(0.01)*empleados_inc)
                tot_cronicos = int(empleados_inc-tot_agudos)

                porc_agudos = Decimal(porc_agudos).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
                porc_cronicos = Decimal(porc_cronicos).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
                porc_dias_trab_tot = 100 - tasa_ausentismo        
                
                
                inc_cant_empls = ausentismos_inc.values('empleado').distinct().count()
                noinc_cant_empls = empleados_tot- inc_cant_empls

                aus_inc = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
                'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot,'porc_agudos':porc_agudos,'porc_cronicos':porc_cronicos,
                'inc_cant_empls':inc_cant_empls,'noinc_cant_empls':noinc_cant_empls,'tot_agudos':tot_agudos,'tot_cronicos':tot_cronicos}

            #AUSENTISMO ACCIDENTES
            ausentismos_acc = ausentismos.filter(tipo_ausentismo=2)
            if ausentismos_acc:
                #empleados_tot = ausentismos_acc.values('empleado').distinct().count()
                # empleados_tot = 77
                dias_caidos_tot=dias_ausentes(fdesde,fhasta,ausentismos_acc) 
                # dias_caidos_tot = 67            
                dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot
                tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)                       
                porc_dias_trab_tot = 100 - tasa_ausentismo        

                tot_accidentes = ausentismos_acc.count()
                acc_empls = ausentismos_acc.values('empleado').distinct().count()
                noacc_empls = empleados_tot- acc_empls

                acc_denunciados = ausentismos_acc.exclude(Q(art_ndenuncia__isnull=True)|Q(art_ndenuncia__exact=''))
                denunciados_empl = acc_denunciados.values('empleado').distinct().count()
                acc_denunciados = (Decimal(acc_denunciados.count()) / Decimal(tot_accidentes))*100 
                acc_sin_denunciar = ausentismos_acc.filter(Q(art_ndenuncia__isnull=True)|Q(art_ndenuncia__exact=''))
                sin_denunciar_empl = acc_sin_denunciar.values('empleado').distinct().count()
                acc_sin_denunciar = (Decimal(acc_sin_denunciar.count()) / Decimal(tot_accidentes))*100 
                
                acc_itinere = ausentismos_acc.filter(art_tipo_accidente=2)
                itinere_empl = acc_itinere.values('empleado').distinct().count()
                acc_itinere = (Decimal(acc_itinere.count()) / Decimal(tot_accidentes))*100                 
                acc_trabajo = ausentismos_acc.filter(art_tipo_accidente=1)
                trabajo_empl = acc_trabajo.values('empleado').distinct().count()
                acc_trabajo = (Decimal(acc_trabajo.count()) / Decimal(tot_accidentes))*100 

                
                aus_acc = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
                'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot,'tot_accidentes':tot_accidentes,'acc_denunciados':acc_denunciados,
                'acc_sin_denunciar':acc_sin_denunciar,'acc_itinere':acc_itinere,'acc_trabajo':acc_trabajo,'acc_empls':acc_empls,'noacc_empls':noacc_empls,
                'denunciados_empl':denunciados_empl,'sin_denunciar_empl':sin_denunciar_empl,'itinere_empl':itinere_empl,'trabajo_empl':trabajo_empl}

            aus_x_grupop = ausentismos.values('aus_grupop__patologia').annotate(total=Count('aus_grupop')).order_by('-total')[:5]
            max_grupop = aus_x_grupop[0]['total']+1
            
            empl_mas_faltadores = []
            for a in ausentismos.select_related('empleado'):
                dias = dias_ausentes_empl(fdesde,fhasta,a)
                empl_mas_faltadores.append({'empleado':a.empleado,'dias':dias})

            empl_mas_faltadores = sorted(empl_mas_faltadores, key = lambda i: i['dias'],reverse=True) 

        context['aus_total']=  aus_total
        context['aus_inc']=  aus_inc
        context['aus_acc']=  aus_acc
        context['aus_x_grupop']=  aus_x_grupop
        context['max_grupop']=  max_grupop
        context['dias_laborables']=  dias_laborables             
        context['empl_mas_faltadores']=  empl_mas_faltadores[:6]             
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
        empresa = None
        if form.is_valid():                                                        
            fdesde = form.cleaned_data['fdesde']   
            fhasta = form.cleaned_data['fhasta']                                                 
            empresa = form.cleaned_data['empresa']                           
            empleado= form.cleaned_data['empleado']                           
            tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     
            trab_cargo= form.cleaned_data['trab_cargo']                           

            ausentismos = ausentismo.objects.filter(baja=False)                      
          
            if fdesde:                
                ausencias = ausentismos.filter(aus_fcrondesde__gte=fdesde)            
            if empresa:
                if empresa.casa_central:
                    ausentismos= ausentismos.filter(empleado__empresa=empresa)
                else:
                    ausentismos= ausentismos.filter(Q(empleado__empresa=empresa)|Q(empleado__empresa__casa_central=empresa))
            else:
                ausentismos= ausentismos.filter(empleado__empresa__pk__in=empresas_habilitadas(self.request))

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
        context['empresa'] = empresa
        dias_laborales = 0
        dias_caidos_tot = 0
        empleados_tot = 0
        dias_trab_tot = 0
        tasa_ausentismo = 0
        aus_total = None
        aus_inc = None
        aus_acc = None
        dias_laborables = 0  
        porc_dias_trab_tot = 100
        inculpables = []
        accidentes = []
        enfermos = []
        import time
        from dateutil.rrule import rrule, MONTHLY
        
        meses = [[int(dt.strftime("%m")),int(dt.strftime("%y"))] for dt in rrule(MONTHLY, dtstart=fdesde, until=fhasta)]
        
        
        # import locale        
        # locale.setlocale(locale.LC_ALL, '')
        listado_meses = ["%s%s" % (MESES[int(dt.strftime("%m"))-1][1].upper(),(dt.strftime("%y"))) for dt in rrule(MONTHLY, dtstart=fdesde, until=fhasta)]
        if empresa:
            empleados_tot = empresa.cantidad_empleados()
        if ausentismos:                                                    
            for m in meses:                
                dias_laborables = int(dias_mes(m[0],m[1],fdesde,fhasta))                 
                ausencias = en_mes_anio(m[0],m[1],ausentismos)
                
                qs_inculpables = ausencias.filter(tipo_ausentismo=1)
                ausenc_inculp = dias_ausentes_mes(m[0],m[1],qs_inculpables)            
                # empl_tot_inculp= qs_inculpables.values('empleado').distinct().count()
                empl_tot_inculp = empleados_tot
                dias_trab_tot = (dias_laborables * empl_tot_inculp)-ausenc_inculp
                if ausenc_inculp >0:                    
                    tasa_inclup =  calcular_tasa_ausentismo(ausenc_inculp,dias_laborables,empl_tot_inculp)                        
                else:
                    tasa_inclup = 0
                inculpables.append(tasa_inclup)
                
                qs_accidentes = ausencias.filter(tipo_ausentismo=2)
                ausenc_acc = dias_ausentes_mes(m[0],m[1],qs_accidentes)  
                # ausenc_acc = qs_accidentes.count()
                # empl_tot_acc= qs_accidentes.values('empleado').distinct().count()
                empl_tot_acc = empleados_tot
                dias_trab_tot = (dias_laborables * empl_tot_acc)-ausenc_acc
                if ausenc_acc >0:
                    tasa_acc =  calcular_tasa_ausentismo(ausenc_acc,dias_laborables,empl_tot_acc)                        
                else:
                    tasa_acc = 0
                accidentes.append(tasa_acc)

                qs_enfermos = ausencias.filter(tipo_ausentismo=3)
                ausenc_enf = dias_ausentes_mes(m[0],m[1],qs_enfermos)  
                # ausenc_enf = qs_enfermos.count()
                # empl_tot_enf= qs_enfermos.values('empleado').distinct().count()
                empl_tot_enf = empleados_tot
                dias_trab_tot = (dias_laborables * empl_tot_enf)-ausenc_enf
                if ausenc_enf >0:
                    tasa_enf =  calcular_tasa_ausentismo(ausenc_enf,dias_laborables,empl_tot_enf)                    
                else:
                    tasa_enf = 0
                enfermos.append(tasa_enf)


        context['inculpables']=  json.dumps(inculpables,cls=DecimalEncoder)        
        context['accidentes']=  json.dumps(accidentes,cls=DecimalEncoder)        
        context['enfermos']=  json.dumps(enfermos,cls=DecimalEncoder)        
        
     
      
        context['listado_meses']=  json.dumps(listado_meses,cls=DecimalEncoder) 
      
        
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


# @login_required 
# def reporte_periodo(request):           
#     template_name = 'reportes/resumen_periodo.html'
#     context = {}
#     context = getVariablesMixin(request) 
#     form = ConsultaPeriodo(request.POST or None,request=request)            
#     fecha = date.today()        
#     fdesde = ultimo_anio()
#     fhasta = hoy()
#     empresa = None
#     if form.is_valid():                                                        
#         fdesde = form.cleaned_data['fdesde']   
#         fhasta = form.cleaned_data['fhasta']                                                 
#         empresa = form.cleaned_data['empresa']                           
#         empleado= form.cleaned_data['empleado']                           
#         tipo_ausentismo = form.cleaned_data['tipo_ausentismo']     
#         trab_cargo= form.cleaned_data['trab_cargo']                           

#         ausentismos = ausentismo.objects.filter(baja=False)                      
                 
#         if empresa:
#             if empresa.casa_central:
#                 ausentismos= ausentismos.filter(empleado__empresa=empresa)
#             else:
#                 ausentismos= ausentismos.filter(Q(empleado__empresa=empresa)|Q(empleado__empresa__casa_central=empresa))
#         else:
#             ausentismos= ausentismos.filter(empleado__empresa__pk__in=empresas_habilitadas(self.request))

#         if empleado:
#             ausentismos= ausentismos.filter(Q(empleado__apellido_y_nombre__icontains=empleado)|Q(empleado__nro_doc__icontains=empleado))
#         if trab_cargo:
#             ausentismos= ausentismos.filter(empleado__trab_cargo=trab_cargo)            

#         if int(tipo_ausentismo) > 0: 
#             ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))

#         ausentismos = ausentismos.filter(Q(aus_fcrondesde__range=[fdesde,fhasta])|Q(aus_fcronhasta__range=[fdesde,fhasta])
#             |Q(aus_fcrondesde__lt=fdesde,aus_fcronhasta__gt=fhasta))  

#     else:
#         ausentismos = None            

#     context['form'] = form
#     context['fecha'] = fecha        
#     context['fdesde'] = fdesde
#     context['fhasta'] = fhasta
#     context['ausentismos'] = ausentismos
#     dias_laborales = 0
#     dias_caidos_tot = 0
#     empleados_tot = 0
#     dias_trab_tot = 0
#     tasa_ausentismo = 0
#     aus_total = None
#     aus_inc = None
#     aus_acc = None
#     dias_laborables = int((fhasta-fdesde).days+1)   
#     porc_dias_trab_tot = 100
#     if empresa:
#         empleados_tot = empresa.cantidad_empleados()
#     if ausentismos:
        
#         #AUSENTISMO TOTAL            
#         #empleados_tot = ausentismos.values('empleado').distinct().count()            
        
#         # dias_caidos_tot = ausentismos.aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)))['dias_caidos'] or 0            
#         dias_caidos_tot=dias_ausentes(fdesde,fhasta,ausentismos)               
#         dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot
#         tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)        
#         porc_dias_trab_tot = 100 - tasa_ausentismo        
        
#         aus_total = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
#         'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot}
#         #F('college_start_date') - F('school_passout_date')
#         #AUSENTISMO INCULPABLE
#         ausentismos_inc = ausentismos.filter(tipo_ausentismo=1)
#         if ausentismos_inc:
#             #empleados_tot = ausentismos_inc.values('empleado').distinct().count()
#             # empleados_tot = 77
#             totales = tot_ausentes_inc(fdesde,fhasta,ausentismos_inc)
#             dias_caidos_tot=totales[0] 
#             # dias_caidos_tot = 67            
#             dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot

#             tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)                                      
            
#             # agudos = ausentismos_inc.filter(aus_diascaidos__lte=30).aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)))['dias_caidos'] or 0
#             # graves = ausentismos_inc.filter(aus_diascaidos__gt=30).aggregate(dias_caidos=Sum(Coalesce('aus_diascaidos', 0)))['dias_caidos'] or 0
#             agudos=totales[1] 
#             graves=totales[2]                 
            
#             porc_agudos = (Decimal(agudos) / Decimal(dias_caidos_tot))*100 
#             porc_cronicos = (Decimal(graves) / Decimal(dias_caidos_tot))*100 

#             porc_agudos = Decimal(porc_agudos).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
#             porc_cronicos = Decimal(porc_cronicos).quantize(Decimal("0.01"), decimal.ROUND_HALF_UP)
#             porc_dias_trab_tot = 100 - tasa_ausentismo        

#             aus_inc = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
#             'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot,'porc_agudos':porc_agudos,'porc_cronicos':porc_cronicos}

#         #AUSENTISMO ACCIDENTES
#         ausentismos_acc = ausentismos.filter(tipo_ausentismo=2)
#         if ausentismos_acc:
#             #empleados_tot = ausentismos_acc.values('empleado').distinct().count()
#             # empleados_tot = 77
#             dias_caidos_tot=dias_ausentes(fdesde,fhasta,ausentismos_acc) 
#             # dias_caidos_tot = 67            
#             dias_trab_tot = (dias_laborables * empleados_tot)-dias_caidos_tot
#             tasa_ausentismo = calcular_tasa_ausentismo(dias_caidos_tot,dias_laborables,empleados_tot)                       
#             porc_dias_trab_tot = 100 - tasa_ausentismo        

#             tot_accidentes = ausentismos_acc.count()
            
#             acc_denunciados = (Decimal(ausentismos_acc.exclude(Q(art_ndenuncia__isnull=True)|Q(art_ndenuncia__exact='')).count()) / Decimal(tot_accidentes))*100 
#             acc_sin_denunciar = (Decimal(ausentismos_acc.filter(Q(art_ndenuncia__isnull=True)|Q(art_ndenuncia__exact='')).count()) / Decimal(tot_accidentes))*100 
#             acc_itinere = (Decimal(ausentismos_acc.filter(art_tipo_accidente=2).count()) / Decimal(tot_accidentes))*100 
#             acc_trabajo = (Decimal(ausentismos_acc.filter(art_tipo_accidente=1).count()) / Decimal(tot_accidentes))*100 
            
#             aus_acc = {'dias_caidos_tot':dias_caidos_tot,'empleados_tot':empleados_tot,'dias_trab_tot':dias_trab_tot,'tasa_ausentismo':tasa_ausentismo,
#             'dias_laborables':dias_laborables,'porc_dias_trab_tot':porc_dias_trab_tot,'tot_accidentes':tot_accidentes,'acc_denunciados':acc_denunciados,
#             'acc_sin_denunciar':acc_sin_denunciar,'acc_itinere':acc_itinere,'acc_trabajo':acc_trabajo}
            

#     context['aus_total']=  aus_total
#     context['aus_inc']=  aus_inc
#     context['aus_acc']=  aus_acc
#     context['dias_laborables']=  dias_laborables
#     if (request.POST.get('submit') == 'Imprimir')and(aus_total):           
#             from django.template.loader import get_template
#             from django.template import RequestContext

#             context = {}
#             context = getVariablesMixin(request)  
#             try:
#               config = configuracion.objects.all().first()
#             except Exception as e:                                                      
#                    messages.error(request,e) 
#             context['aus_total'] = aus_total
#             context['aus_inc']=  aus_inc
#             context['aus_acc']=  aus_acc
#             context['dias_laborables']=  dias_laborables
#             context['config'] = config
#             context['fecha'] = fecha        
#             context['fdesde'] = fdesde
#             context['fhasta'] = fhasta
#             context['ausentismos'] = ausentismos            
            
#             # template_name = 'reportes/reporte_periodo.html'            
#             html_template = get_template(template_name)
#             rendered_html = html_template.render({'aus_total':aus_total}).encode(encoding="UTF-8")            
            
#             # return render_to_pdf_response(request, template_name, context) 
#             return render(request,template_name, context) 
#     return render(request,template_name, context) 




######################################################################################
import calendar

def en_mes_anio(mes, anio,ausentismos):
    d_fmt = "{0:>02}/{1:>02}/{2}"
    fdesde = datetime.strptime(d_fmt.format(1, mes, anio), '%d/%m/%y').date()
    ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
    fhasta = datetime.strptime(d_fmt.format(ultimo_dia_mes, mes, anio), '%d/%m/%y').date()
    ausencias = ausentismos.filter(
        Q(aus_fcrondesde__range=[fdesde,fhasta])|Q(aus_fcronhasta__range=[fdesde,fhasta])
        |Q(aus_fcrondesde__lt=fdesde,aus_fcronhasta__gt=fhasta))    
    return ausencias

def dias_mes(mes, anio,fdesde,fhasta):
     d_fmt = "{0:>02}/{1:>02}/{2}"
     fini = datetime.strptime(d_fmt.format(1, mes, anio), '%d/%m/%y').date()
     ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
     ffin = datetime.strptime(d_fmt.format(ultimo_dia_mes, mes, anio), '%d/%m/%y').date()
     if fdesde>=fini:
        fini=fdesde
     if fhasta<=ffin:
        ffin =fhasta

     return (ffin-fini).days+1

def dias_ausentes(fdesde,fhasta,ausentismos):     
    tot=0
    for a in ausentismos:
        fini = a.aus_fcrondesde     
        ffin = a.aus_fcronhasta
        
        if fdesde>=fini:
            fini=fdesde
        if fhasta<=ffin:
            ffin =fhasta        
        tot+=(ffin-fini).days+1        
    return tot

def dias_ausentes_empl(fdesde,fhasta,a):     
    tot=0
    fini = a.aus_fcrondesde     
    ffin = a.aus_fcronhasta        
    if fdesde>=fini:
        fini=fdesde
    if fhasta<=ffin:
        ffin =fhasta        
    tot=(ffin-fini).days+1
    return tot

def dias_ausentes_mes(mes, anio,ausentismos):     
    tot=0
    d_fmt = "{0:>02}/{1:>02}/{2}"
    fdesde = datetime.strptime(d_fmt.format(1, mes, anio), '%d/%m/%y').date()
    ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
    fhasta = datetime.strptime(d_fmt.format(ultimo_dia_mes, mes, anio), '%d/%m/%y').date()
    for a in ausentismos:
        fini = a.aus_fcrondesde     
        ffin = a.aus_fcronhasta
        if fdesde>=fini:
            fini=fdesde
        if fhasta<=ffin:
            ffin =fhasta
        tot+=(ffin-fini).days+1
    return tot    



def tot_ausentes_inc(fdesde,fhasta,ausentismos):         
    parcial=0
    agudos=0
    graves=0
    tot=0
    for a in ausentismos:
        fini = a.aus_fcrondesde     
        ffin = a.aus_fcronhasta
        
        if fdesde>=fini:
            fini=fdesde
        if fhasta<=ffin:
            ffin =fhasta        
        parcial=(ffin-fini).days+1        
        tot+=parcial
        if parcial <= 30:
            agudos+=parcial
        else:
            graves+=parcial
    return [tot,agudos,graves]