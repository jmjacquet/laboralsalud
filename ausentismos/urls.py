# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^ausentismo/$', AusentismoView.as_view(),name="ausentismo_listado"),
    url(r'^ausentismo/nuevo/$', AusentismoCreateView.as_view(), name="ausentismo_nuevo"),
    url(r'^ausentismo/editar/(?P<id>\d+)/$', AusentismoEditView.as_view(), name="ausentismo_editar"),    
    url(r'^ausentismo/detalles/(?P<id>\d+)/$', AusentismoVerView.as_view(), name="ausentismo_detalles"),    
    url(r'^ausentismo/baja_alta/(?P<id>\d+)/$', ausentismo_baja_alta, name='ausentismo_baja_alta'),
]