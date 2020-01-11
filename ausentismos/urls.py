# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^$', AusentismoView.as_view(),name="ausentismo_listado"),
    url(r'^nuevo/$', AusentismoCreateView.as_view(), name="ausentismo_nuevo"),
    url(r'^editar/(?P<id>\d+)/$', AusentismoEditView.as_view(), name="ausentismo_editar"),    
    url(r'^detalles/(?P<id>\d+)/$', AusentismoVerView.as_view(), name="ausentismo_detalles"),    
    url(r'^eliminar/(?P<id>\d+)/$', ausentismo_eliminar, name='ausentismo_eliminar'),

    url(r'^historial/(?P<id>\d+)/$', AusentismoHistorialView.as_view(), name="ausentismo_historial"),    

    url(r'^patologia/$', PatologiaView.as_view(),name="patologia_listado"),
    url(r'^patologia/nuevo/$', PatologiaCreateView.as_view(), name="patologia_nuevo"),
    url(r'^patologia/editar/(?P<id>\d+)/$', PatologiaEditView.as_view(), name="patologia_editar"),        
    url(r'^patologia/baja_alta/(?P<id>\d+)/$', patologia_baja_alta, name='patologia_baja_alta'),

    url(r'^diagnostico/$', DiagnosticoView.as_view(),name="diagnostico_listado"),
    url(r'^diagnostico/nuevo/$', DiagnosticoCreateView.as_view(), name="diagnostico_nuevo"),
    url(r'^diagnostico/editar/(?P<id>\d+)/$', DiagnosticoEditView.as_view(), name="diagnostico_editar"),    
    # url(r'^diagnostico/detalles/(?P<id>\d+)/$', ARTVerView.as_view(), name="patologia_detalles"),    
    url(r'^diagnostico/baja_alta/(?P<id>\d+)/$', diagnostico_baja_alta, name='diagnostico_baja_alta'),
    
    url(r'^ausencias_importar/$', ausencias_importar,name="ausencias_importar"),
    url(r'^generarInforme/$',generarInforme,name="generarInforme"),
    url(r'^ausentismo_eliminar_masivo/$',ausentismo_eliminar_masivo,name="ausentismo_eliminar_masivo"),
]