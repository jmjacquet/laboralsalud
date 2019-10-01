# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

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

