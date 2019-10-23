# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
import datetime
from laboralsalud.utilidades import *
from entidades.models import ent_art,ent_cargo,ent_especialidad,ent_medico_prof,ent_empresa,ent_empleado

class ConsultaPeriodo(forms.Form):               	
	fdesde =  forms.DateField(label='Fecha Desde',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=inicioMes())
	fhasta =  forms.DateField(label='Fecha Hasta',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=finMes())    	
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),required=False)
	empleado = forms.CharField(label='Empleado',max_length=100,widget=forms.TextInput(attrs={'class':'form-control','text-transform': 'uppercase'}),required=False)	
	tipo_ausentismo = forms.ChoiceField(label='Estado',choices=TIPO_AUSENCIA_,required=False,initial=0)	
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ConsultaPeriodo, self).__init__(*args, **kwargs)						
		# self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False)