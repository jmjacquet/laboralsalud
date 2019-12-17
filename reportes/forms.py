# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
import datetime
from laboralsalud.utilidades import *
from entidades.models import ent_art,ent_cargo,ent_especialidad,ent_medico_prof,ent_empresa,ent_empleado


class ConsultaPeriodo(forms.Form):               	
	fdesde =  forms.DateField(label='Fecha Desde',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=inicioMes())
	fhasta =  forms.DateField(label='Fecha Hasta',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=finMes())    	
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),empty_label='Todas',required=False)
	empleado = forms.CharField(required=False,label='Empleado')	
	tipo_ausentismo = forms.ChoiceField(label='Tipo Ausentismo',choices=TIPO_AUSENCIA_,required=False,initial=0)	
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ConsultaPeriodo, self).__init__(*args, **kwargs)						
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))