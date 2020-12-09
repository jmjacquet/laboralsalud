# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
import datetime
from laboralsalud.utilidades import *
from entidades.models import ent_art,ent_cargo,ent_especialidad,ent_medico_prof,ent_empresa,ent_empleado
from entidades.forms import TrabajoModelChoiceField

def mes_anio(fecha):
	return fecha.strftime("%m/%Y")

class ConsultaPeriodo(forms.Form):               	
	periodo =  forms.DateField(label='Período',input_formats=['%m/%Y'],widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=mes_anio(inicioMes()))
	#fdesde =  forms.DateField(label='Fecha Desde',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=inicioMes())
	#fhasta =  forms.DateField(label='Fecha Hasta',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=finMes())    	
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),initial=0,required=True)
	empleado = forms.CharField(required=False,label='Empleado')	
	tipo_ausentismo = forms.ChoiceField(label='Tipo Ausentismo',choices=TIPO_AUSENCIA_,required=False,initial=0)	
	trab_cargo = TrabajoModelChoiceField(label=u'Puesto de Trabajo',queryset=ent_cargo.objects.filter(baja=False),required=False,)
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ConsultaPeriodo, self).__init__(*args, **kwargs)						
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))

class ConsultaAnual(forms.Form):               	
	periodo_desde =  forms.DateField(label='Período Desde',input_formats=['%m/%Y'],widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=mes_anio(inicioAnio()))
	periodo_hasta =  forms.DateField(label='Período Hasta',input_formats=['%m/%Y'],widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=mes_anio(finMes()))
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),required=True,initial=0)
	empleado = forms.CharField(required=False,label='Empleado')	
	tipo_ausentismo = forms.ChoiceField(label='Tipo Ausentismo',choices=TIPO_AUSENCIA_,required=False,initial=0)	
	trab_cargo = TrabajoModelChoiceField(label=u'Puesto de Trabajo',queryset=ent_cargo.objects.filter(baja=False),required=False,)
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ConsultaAnual, self).__init__(*args, **kwargs)						
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))		