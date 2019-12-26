# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^art/$', ARTView.as_view(),name="art_listado"),
    url(r'^art/nuevo/$', ARTCreateView.as_view(), name="art_nuevo"),
    url(r'^art/editar/(?P<id>\d+)/$', ARTEditView.as_view(), name="art_editar"),    
    url(r'^art/detalles/(?P<id>\d+)/$', ARTVerView.as_view(), name="art_detalles"),    
    url(r'^art/baja_alta/(?P<id>\d+)/$', art_baja_alta, name='art_baja_alta'),

    url(r'^cargo/$', CargoView.as_view(),name="cargo_listado"),
    url(r'^cargo/nuevo/$', CargoCreateView.as_view(), name="cargo_nuevo"),
    url(r'^cargo/editar/(?P<id>\d+)/$', CargoEditView.as_view(), name="cargo_editar"),    
    url(r'^cargo/detalles/(?P<id>\d+)/$', CargoVerView.as_view(), name="cargo_detalles"),    
    url(r'^cargo/baja_alta/(?P<id>\d+)/$', cargo_baja_alta, name='cargo_baja_alta'),

    url(r'^especialidad/$', EspecialidadView.as_view(),name="especialidad_listado"),
    url(r'^especialidad/nuevo/$', EspecialidadCreateView.as_view(), name="especialidad_nuevo"),
    url(r'^especialidad/editar/(?P<id>\d+)/$', EspecialidadEditView.as_view(), name="especialidad_editar"),    
    url(r'^especialidad/detalles/(?P<id>\d+)/$', EspecialidadVerView.as_view(), name="especialidad_detalles"),    
    url(r'^especialidad/baja_alta/(?P<id>\d+)/$', especialidad_baja_alta, name='especialidad_baja_alta'),

    url(r'^medico_prof/$', MedProfView.as_view(),name="medico_prof_listado"),
    url(r'^medico_prof/nuevo/$', MedProfCreateView.as_view(), name="medico_prof_nuevo"),
    url(r'^medico_prof/editar/(?P<id>\d+)/$', MedProfEditView.as_view(), name="medico_prof_editar"),    
    url(r'^medico_prof/detalles/(?P<id>\d+)/$', MedProfVerView.as_view(), name="medico_prof_detalles"),    
    url(r'^medico_prof/baja_alta/(?P<id>\d+)/$', medico_prof_baja_alta, name='medico_prof_baja_alta'),

    url(r'^empresa/$', EmpresaView.as_view(),name="empresa_listado"),
    url(r'^empresa/nuevo/$', EmpresaCreateView.as_view(), name="empresa_nuevo"),
    url(r'^empresa/editar/(?P<id>\d+)/$', EmpresaEditView.as_view(), name="empresa_editar"),    
    url(r'^empresa/detalles/(?P<id>\d+)/$', EmpresaVerView.as_view(), name="empresa_detalles"),    
    url(r'^empresa/baja_alta/(?P<id>\d+)/$', empresa_baja_alta, name='empresa_baja_alta'),

    url(r'^empleado/$', EmpleadoView.as_view(),name="empleado_listado"),
    url(r'^empleado/nuevo/$', EmpleadoCreateView.as_view(), name="empleado_nuevo"),
    url(r'^empleado/editar/(?P<id>\d+)/$', EmpleadoEditView.as_view(), name="empleado_editar"),    
    url(r'^empleado/detalles/(?P<id>\d+)/$', EmpleadoVerView.as_view(), name="empleado_detalles"),    
    url(r'^empleado/baja_alta/(?P<id>\d+)/$', empleado_baja_alta, name='empleado_baja_alta'),

    url(r'^importar_empleados/$', importar_empleados,name="importar_empleados"),
]
