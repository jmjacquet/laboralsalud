# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import ent_art,ent_cargo,ent_especialidad,ent_medico_prof,ent_empresa,ent_empleado
from datetime import datetime, timedelta,date
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
	apellido_y_nombre = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),required=True)
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
			

	def clean(self):		
		cuit = self.cleaned_data.get('cuit')	
		if cuit:
			if not validar_cuit(str(cuit)):
				raise forms.ValidationError("El Nº de CUIT ingresado es incorrecto! Verifique.")
				
		tipo_form = self.cleaned_data.get('tipo_form')
		if tipo_form == 'ALTA':			
			if cuit: 
				try:
					entidad=ent_medico_prof.objects.filter(cuit=cuit)				
					if entidad:
						raise forms.ValidationError("El Nº de CUIT ingresado ya existe en el Sistema! Verifique.")
				except ent_medico_prof.DoesNotExist:
				#because we didn't get a match
					pass
		return self.cleaned_data


class EmpresaForm(forms.ModelForm):		
	cuit = forms.IntegerField(label='CUIT',required = False,widget=PostPendWidgetBuscar(attrs={'class':'form-control','autofocus':'autofocus'},
			base_widget=TextInput,data='<i class="fa fa-search" aria-hidden="true"></i>',tooltip=u"Buscar datos y validar CUIT en AFIP"))				
	cod_postal = forms.IntegerField(label='CP',required = False)			
	observaciones = forms.CharField(label='Observaciones / Datos adicionales',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 5}),required = False)	
	razon_social = forms.CharField(required=True)
	codigo = forms.CharField(required=True)
	# tipo_form = forms.CharField(widget = forms.HiddenInput(), required = False)	
	class Meta:
			model = ent_empresa
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(EmpresaForm, self).__init__(*args, **kwargs)		

class TrabajoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return obj.get_cargo()

class EmpleadoForm(forms.ModelForm):		
	apellido_y_nombre = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),required=True)
	nro_doc = forms.IntegerField(label=u'Documento',required = True)		
	cod_postal = forms.IntegerField(label='CP',required = False)			
	observaciones = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 10}),required = False)	
	fecha_nac = forms.DateField(label=u'Fecha Nacim.',required = True,widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
	empr_fingreso = forms.DateField(label=u'F.Ingreso.',required = False,widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
	empr_antig = forms.CharField(label=u'Antig.(años)',widget=forms.TextInput(attrs={'readonly': 'readonly'}),required=False)
	trab_fingreso = forms.DateField(label=u'F.Ingreso',required = False,widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
	trab_antig = forms.CharField(label=u'Antig.(años)',widget=forms.TextInput(attrs={'readonly': 'readonly'}),required=False)
	trab_fbaja = forms.DateField(label=u'Fecha Baja',required = False,widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
	trab_preocup_conclus = forms.CharField(label=u'Conclusión Preocupacional',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	trab_factores_riesgo = forms.CharField(label=u'Factores de Riesgo a lo que está Expuesto',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	trab_tareas_dif_det = forms.CharField(label=u'Descripción Tareas Diferentes',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	trab_anteriores = forms.CharField(label=u'Trabajos Anteriores',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	trab_antecedentes = forms.CharField(label=u'Antecedentes Patológicos',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	trab_accidentes = forms.CharField(label=u'Accidentes ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	trab_vacunas = forms.CharField(label=u'Vacunas',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	trab_armas = forms.ChoiceField(label=u'¿Portación de Armas?',choices=SINO,required=True,initial='N')
	trab_tareas_dif = forms.ChoiceField(label=u'¿Tareas Diferentes?',choices=SINO,required=True,initial='N')
	trab_preocupac = forms.ChoiceField(label='¿Preocupacional?',choices=SINO,required=True,initial='N')
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),required=True)
	trab_cargo = TrabajoModelChoiceField(label=u'Puesto de Trabajo',queryset=ent_cargo.objects.filter(baja=False),required=False,)
					
	class Meta:
			model = ent_empleado
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(EmpleadoForm, self).__init__(*args, **kwargs)
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))				

	def clean(self):		
		trab_preocupac = self.cleaned_data.get('trab_preocupac')	
		trab_preocup_fecha = self.cleaned_data.get('trab_preocup_fecha')	
		if (trab_preocupac=='S') and (not trab_preocup_fecha):
				self.add_error("trab_preocup_fecha",u'¡Debe cargar una Fecha!')

		trab_fingreso = self.cleaned_data.get('trab_fingreso')	
		trab_fbaja = self.cleaned_data.get('trab_fbaja')	
		empr_fingreso = self.cleaned_data.get('empr_fingreso')	

		if trab_fingreso:
			if date.today() < trab_fingreso:
				self.add_error("trab_fingreso",u'¡Verifique las Fechas!')

		if empr_fingreso:
			if date.today() < empr_fingreso:
				self.add_error("empr_fingreso",u'¡Verifique las Fechas!')
        	

		if trab_fingreso and trab_fbaja:			
			if trab_fingreso > trab_fbaja:
				self.add_error("trab_fbaja",u'¡Verifique las Fechas!')
						
		return self.cleaned_data


class ConsultaEmpleados(forms.Form):               		
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),empty_label='Todas',required=False)
	estado = forms.ChoiceField(label='Estado',choices=ESTADO_,required=False,initial=0)	
	art = forms.ModelChoiceField(label='ART',queryset=ent_art.objects.filter(baja=False),empty_label='Todas',required=False)
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ConsultaEmpleados, self).__init__(*args, **kwargs)					
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))


class ImportarEmpleadosForm(forms.Form):
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),empty_label='----',required=True)
	archivo = forms.FileField(label='Seleccione un archivo',required=True)  
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ImportarEmpleadosForm, self).__init__(*args, **kwargs)					
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))

	def clean(self):
		archivo = self.cleaned_data.get('archivo')        
		if not archivo.name.endswith('.csv'):
			self.add_error("archivo",u'¡El archivo debe tener extensión .CSV!')            
		#if file is too large, return
		if archivo.multiple_chunks():
			self.add_error("archivo",u"El archivo es demasiado grande (%.2f MB)." % (archivo.size/(1000*1000),))
		return self.cleaned_data
	    

