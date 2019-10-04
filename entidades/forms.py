# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import ent_art,ent_cargo,ent_especialidad,ent_medico_prof,ent_empresa

from laboralsalud.utilidades import *

class ARTForm(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),required=True)	
	codigo = forms.CharField(required=True)	
	class Meta:
			model = ent_art
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(ARTForm, self).__init__(*args, **kwargs)				


class CargoForm(forms.ModelForm):	
	class Meta:
			model = ent_cargo
			exclude = ['id','baja']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(CargoForm, self).__init__(*args, **kwargs)				

class EspecialidadForm(forms.ModelForm):	
	class Meta:
			model = ent_especialidad
			exclude = ['id','baja']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(EspecialidadForm, self).__init__(*args, **kwargs)	



class MedProfForm(forms.ModelForm):		
	cuit = forms.IntegerField(label='CUIT',required = False,widget=PostPendWidgetBuscar(attrs={'class':'form-control','autofocus':'autofocus'},
			base_widget=TextInput,data='<i class="fa fa-search" aria-hidden="true"></i>',tooltip=u"Buscar datos y validar CUIT en AFIP"))			
	nro_doc = forms.IntegerField(label=u'Documento',required = True)		
	cod_postal = forms.IntegerField(label='CP',required = False)			
	observaciones = forms.CharField(label='Observaciones / Datos adicionales',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 5}),required = False)	
	tipo_form = forms.CharField(widget = forms.HiddenInput(), required = False)	
	class Meta:
			model = ent_medico_prof
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(MedProfForm, self).__init__(*args, **kwargs)				
			

	# def clean(self):		
	# 	cuit = self.cleaned_data.get('cuit')	
	# 	if cuit:
	# 		if not validar_cuit(str(cuit))
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



class EmpresaForm(forms.ModelForm):		
	cuit = forms.IntegerField(label='CUIT',required = False,widget=PostPendWidgetBuscar(attrs={'class':'form-control','autofocus':'autofocus'},
			base_widget=TextInput,data='<i class="fa fa-search" aria-hidden="true"></i>',tooltip=u"Buscar datos y validar CUIT en AFIP"))				
	cod_postal = forms.IntegerField(label='CP',required = False)			
	observaciones = forms.CharField(label='Observaciones / Datos adicionales',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 5}),required = False)	
	# tipo_form = forms.CharField(widget = forms.HiddenInput(), required = False)	
	class Meta:
			model = ent_empresa
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(EmpresaForm, self).__init__(*args, **kwargs)		