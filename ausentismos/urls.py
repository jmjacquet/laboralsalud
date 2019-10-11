# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^$', AusentismoView.as_view(),name="ausentismo_listado"),
    url(r'^nuevo/$', AusentismoCreateView.as_view(), name="ausentismo_nuevo"),
    url(r'^editar/(?P<id>\d+)/$', AusentismoEditView.as_view(), name="ausentismo_editar"),    
    url(r'^detalles/(?P<id>\d+)/$', AusentismoVerView.as_view(), name="ausentismo_detalles"),    
    url(r'^baja_alta/(?P<id>\d+)/$', ausentismo_baja_alta, name='ausentismo_baja_alta'),
]