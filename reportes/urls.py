# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
urlpatterns = [ 
    
    url(r'^reporte_resumen_periodo/$', reporte_resumen_periodo, name='reporte_resumen_periodo'),
    url(r'^reporte_resumen_anual/$', reporteResumenAnual, name='reporte_resumen_anual'),


]
