# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
urlpatterns = [ 
    url(r'^reporte_resumen_periodo/$', ReporteResumenPeriodo.as_view(), name='reporte_resumen_periodo'),
]