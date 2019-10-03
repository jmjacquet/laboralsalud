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
]
