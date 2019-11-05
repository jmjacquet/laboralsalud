# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^$', PrincipalView.as_view(), name='principal'),
    url(r'^buscarDatosAPICUIT/$', buscarDatosAPICUIT, name='buscarDatosAPICUIT'),
    url(r'^buscarDatosEntidad/$', buscarDatosEntidad, name='buscarDatosEntidad'),
    url(r'^recargar_empleados/$', recargar_empleados, name='recargar_empleados'),
    url(r'^recargar_empleados_empresa/(?P<id>\d+)/$', recargar_empleados_empresa, name='recargar_empleados_empresa'),
    url(r'^recargar_medicos/$', recargar_medicos, name='recargar_medicos'),
    url(r'^recargar_diagnosticos/$', recargar_diagnosticos, name='recargar_diagnosticos'),
    url(r'^recargar_patologias/$', recargar_patologias, name='recargar_patologias'),

    url(r'^turnos/$', TurnosView.as_view(),name="turnos_listado"),
    url(r'^turnos/nuevo/$', TurnosCreateView.as_view(), name="turnos_nuevo"),
    url(r'^turnos/editar/(?P<id>\d+)/$', TurnosEditView.as_view(), name="turnos_editar"),    
]
