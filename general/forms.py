# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import ent_art,ent_cargo,ent_especialidad,ent_medico_prof,ent_empresa,ent_empleado,turnos
from datetime import datetime, timedelta,date
from laboralsalud.utilidades import *


class LoginForm(forms.Form):
	usuario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','text-transform': 'uppercase','autofocus':'autofocus'}),required = True)
	password = forms.CharField(widget=forms.PasswordInput(),required=True)
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False,casa_central__isnull=True),empty_label='Administrador',required=False)

class EmpleadoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return obj.get_empleado()

class TurnosForm(forms.ModelForm):		
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),empty_label='---',required=True)
	empleado = EmpleadoModelChoiceField(label='Empleado',queryset=ent_empleado.objects.filter(baja=False),empty_label='---',required = True)	
	fecha =  forms.DateField(label='Fecha',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=hoy())
	hora =  forms.TimeField(label='Hora',widget=forms.TimeInput(attrs={'class': 'form-control'}),required = True)
	observaciones = forms.CharField(label='Observaciones / Datos adicionales',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 5}),required = False)	
	tipo_form = forms.CharField(widget = forms.HiddenInput(), required = False)	
	estado = forms.ChoiceField(label='Estado',choices=ESTADO_TURNO,required=True,initial=0)
	class Meta:
			model = turnos
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(TurnosForm, self).__init__(*args, **kwargs)						
		self.fields['empleado'].queryset = ent_empleado.objects.filter(baja=False,empresa__pk__in=empresas_habilitadas(request))
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request),casa_central__isnull=True)				
			

	# def clean(self):		
	# 	cuit = self.cleaned_data.get('cuit')	
	# 	if cuit:
	# 		if not validar_cuit(str(cuit)):
	# 			raise forms.ValidationError("El Nº de CUIT ingresado es incorrecto! Verifique.")
				
	# 	tipo_form = self.cleaned_data.get('tipo_form')
	# 	if tipo_form == 'ALTA':			
	# 		if cuit: 
	# 			try:
	# 				entidad=ent_medico_prof.objects.filter(cuit=cuit)				
	# 				if entidad:
	# 					raise forms.ValidationError("El Nº de CUIT ingresado ya existe en el Sistema! Verifique.")
	# 			except ent_medico_prof.DoesNotExist:
	# 			#because we didn't get a match
	# 				pass
	# 	return self.cleaned_data



class ConsultaTurnos(forms.Form):               	
	fdesde =  forms.DateField(label='Fecha Desde',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=inicioMes())
	fhasta =  forms.DateField(label='Fecha Hasta',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=finMes())    	
	qempresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),empty_label='Todas',required=False)
	qempleado = forms.CharField(required=False,label='Empleado')	
	qestado = forms.ChoiceField(label='Estado',choices=ESTADO_TURNO_,required=False,initial=3)
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ConsultaTurnos, self).__init__(*args, **kwargs)			
		self.fields['qempresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))


class ConsultaFechasInicio(forms.Form):               	
	fecha1 =  forms.DateField(label='',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=hoy())	
	fecha2 =  forms.DateField(label='',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = True,initial=hoy())	
	

	
		