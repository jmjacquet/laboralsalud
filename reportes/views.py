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
from decimal import *

################################################################

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
                ausentismos= ausentismos.filter(fecha_creacion__gte=fdesde)            
            if fhasta:
                ausentismos= ausentismos.filter(fecha_creacion__lte=fhasta)           
            if empresa:
                ausentismos= ausentismos.filter(empleado__empresa=empresa)            
            if empleado:
                ausentismos= ausentismos.filter(empleado__apellido_y_nombre__icontains=empleado)

            if int(tipo_ausentismo) > 0: 
                ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))


        else:
            
            ausentismos = None            

        context['form'] = form
        context['fecha'] = fecha        
        context['fdesde'] = fdesde
        context['fhasta'] = fhasta
        context['ausentismos'] = ausentismos
        aus_total = None
        if ausentismos:
                        
            aus_total = ausentismos.annotate(dias_caidos=Sum('aus_diascaidos',output_field=IntegerField()),cant_empl=Count('empleado',output_field=IntegerField()))
        #     ventas = cpbs.filter(cpb_tipo__compra_venta='V').annotate(pendiente=Sum(F('saldo')*F('cpb_tipo__signo_ctacte'),output_field=DecimalField()),saldado=Sum((F('importe_total')-F('saldo'))*F('cpb_tipo__signo_ctacte'),output_field=DecimalField())).order_by(F('m'))
        #     compras = cpbs.filter(cpb_tipo__compra_venta='C').annotate(pendiente=Sum(F('saldo')*F('cpb_tipo__signo_ctacte'),output_field=DecimalField()),saldado=Sum((F('importe_total')-F('saldo'))*F('cpb_tipo__signo_ctacte'),output_field=DecimalField())).order_by(F('m'))

        #     for v in ventas:
        #         ventas_deuda.append(v['pendiente'])
        #         ventas_pagos.append(v['saldado'])

        #     for c in compras:
        #         compras_deuda.append(c['pendiente'])
        #         compras_pagos.append(c['saldado'])
            



        #     cpb_detalles = cpb_comprobante_detalle.objects.filter(cpb_comprobante__in=comprobantes)
        #     productos_vendidos = cpb_detalles.filter(cpb_comprobante__cpb_tipo__compra_venta='V')
        #     productos_vendidos_total = productos_vendidos.aggregate(sum=Sum(F('importe_total')*F('cpb_comprobante__cpb_tipo__signo_ctacte'), output_field=DecimalField()))['sum'] or 0 
        #     productos_vendidos = productos_vendidos.values('producto__nombre').annotate(tot=Sum(F('importe_total')*F('cpb_comprobante__cpb_tipo__signo_ctacte'),output_field=DecimalField())).order_by('-tot')[:10]
        #     context['productos_vendidos'] = productos_vendidos

        #     productos_comprados = cpb_detalles.filter(cpb_comprobante__cpb_tipo__compra_venta='C')
        #     productos_comprados_total = productos_comprados.aggregate(sum=Sum(F('importe_total')*F('cpb_comprobante__cpb_tipo__signo_ctacte'), output_field=DecimalField()))['sum'] or 0 
        #     productos_comprados = productos_comprados.values('producto__nombre').annotate(tot=Sum(F('importe_total')*F('cpb_comprobante__cpb_tipo__signo_ctacte'),output_field=DecimalField())).order_by('-tot')[:10]
        #     context['productos_comprados'] = productos_comprados
                    
        #     ranking_vendedores = comprobantes.values('vendedor__apellido_y_nombre').annotate(tot=Sum(F('importe_total'),output_field=DecimalField())).order_by('-tot')[:10]
        #     context['ranking_vendedores'] = ranking_vendedores

        #     ranking_clientes = comprobantes.filter(cpb_tipo__compra_venta='V').values('entidad__apellido_y_nombre').annotate(tot=Sum(F('importe_total')*F('cpb_tipo__signo_ctacte'),output_field=DecimalField())).order_by('-tot')[:10]
        #     context['ranking_clientes'] = ranking_clientes

        #     ranking_proveedores = comprobantes.filter(cpb_tipo__compra_venta='C').values('entidad__apellido_y_nombre').annotate(tot=Sum(F('importe_total')*F('cpb_tipo__signo_ctacte'),output_field=DecimalField())).order_by('-tot')[:10]
        #     context['ranking_proveedores'] = ranking_proveedores

        # context['meses']= json.dumps(meses,cls=DecimalEncoder)       
        context['aus_total']=  json.dumps(aus_total,cls=DecimalEncoder)
        # context['ventas_pagos']=  json.dumps(ventas_pagos,cls=DecimalEncoder)
        # context['compras_deuda']= json.dumps(compras_deuda,cls=DecimalEncoder)
        # context['compras_pagos']= json.dumps(compras_pagos,cls=DecimalEncoder)

        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
