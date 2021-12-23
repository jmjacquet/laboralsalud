# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import ent_art,ent_cargo,ent_especialidad,ent_medico_prof,ent_empresa,ent_empleado,turnos,configuracion
from datetime import datetime, timedelta,date
from laboralsalud.utilidades import *

	
class EmpresasLoginModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return u'%s' % unicode(obj.razon_social.upper().replace(" (CC)",""))

class LoginForm(forms.Form):
	usuario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','text-transform': 'uppercase','autofocus':'autofocus'}),required = True)
	password = forms.CharField(widget=forms.PasswordInput(),required=True)
	empresa = EmpresasLoginModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False,casa_central__isnull=True),empty_label='Administrador',required=False)

class EmpleadoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return obj.get_empleado()

class TurnosForm(forms.ModelForm):		
	empresa = forms.ModelChoiceField(label='Empresa',queryset=None,empty_label='---',required=True)
	empleado = EmpleadoModelChoiceField(label='Empleado',queryset=None,empty_label='---',required = True)	
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
		empresas = empresas_habilitadas(request)
		self.fields['empleado'].queryset = ent_empleado.objects.filter(baja=False,empresa__pk__in=empresas)
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas)				
			

	def clean(self):		
	 	fecha = self.cleaned_data.get('fecha')	
	 	if not fecha:
			self.add_error("fecha", u'¡Fecha no válida!')
	 	if fecha<hoy():
	 		self.add_error("fecha",u'¡Fecha no válida!')
		return self.cleaned_data



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
	

	
class ConfiguracionForm(forms.ModelForm):	
	cuit = forms.CharField(label='CUIT',required = False,widget=PostPendWidgetBuscar(attrs={'class':'form-control','autofocus':'autofocus'},
			base_widget=NumberInput,data='<i class="fa fa-search" aria-hidden="true"></i>',tooltip=u"Buscar datos y validar CUIT en AFIP"))		
	fecha_inicio_activ = forms.DateField(label='Inicio Actividades',required = True,widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),initial=inicioMes())	
	mail_cuerpo = forms.CharField(label=u'Cuerpo Email (envío de Comprobantes)',widget=forms.Textarea(attrs={ 'class':'form-control2','rows': 3}),required = False)				
	mail_password = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=20,label=u'Contraseña')     	
	class Meta:
			model = configuracion
			exclude = ['id']	

	def __init__(self, *args, **kwargs):
		super(ConfiguracionForm, self).__init__(*args, **kwargs)		
		