# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import *
from entidades.models import ent_empleado,ent_medico_prof
from laboralsalud.utilidades import *


class EmpleadoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return obj.get_empleado()

class MedicoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return obj.get_medico()

class PatologiaForm(forms.ModelForm):
	patologia = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),required=True)	
	codigo = forms.CharField(required=True)	
	class Meta:
			model = aus_patologia
			exclude = ['id','baja']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(PatologiaForm, self).__init__(*args, **kwargs)		

class DiagnosticoForm(forms.ModelForm):
	diagnostico = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),required=True)	
	codigo = forms.CharField(required=True)	
	class Meta:
			model = aus_diagnostico
			exclude = ['id','baja']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(DiagnosticoForm, self).__init__(*args, **kwargs)					

class AusentismoForm(forms.ModelForm):
	empleado = EmpleadoModelChoiceField(label='',queryset=ent_empleado.objects.filter(baja=False),empty_label='---',required = False)		
	tipo_ausentismo = forms.ChoiceField(label='',choices=TIPO_AUSENCIA,required=False,initial=1)
	tipo_control = forms.ChoiceField(label='',choices=TIPO_CONTROL,required=False,initial='C')
	aus_control = forms.ChoiceField(label=u'¿Asistió a Control?',choices=SINO,required=False,initial='N')
	aus_certificado = forms.ChoiceField(label=u'¿Presenta Certificado?',choices=SINO,required=False,initial='N')
	observaciones = forms.CharField(label='Observaciones Generales',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	descr_altaparc = forms.CharField(label=u'Características de Alta con Restricción',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	detalle_acc_art = forms.CharField(label='Detalle Accidente ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	estudios_partic = forms.CharField(label=u'Estudios Particulares',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	estudios_art = forms.CharField(label='Estudios ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	recalificac_art = forms.CharField(label=u'Recalificación ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	aus_grupop = forms.ModelChoiceField(label=u'Grupo Patológico',queryset=aus_patologia.objects.filter(baja=False),required=False)
	aus_diagn = forms.ModelChoiceField(label=u'Diagnóstico',queryset=aus_diagnostico.objects.filter(baja=False),required=False)
	aus_medico = MedicoModelChoiceField(label=u'Médico Tratante',queryset=ent_medico_prof.objects.filter(baja=False),required=False)
	art_medico = MedicoModelChoiceField(label=u'Médico ART',queryset=ent_medico_prof.objects.filter(baja=False),required=False)
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),required=False)
	aus_fcontrol = forms.DateField(label='Fecha Control',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	aus_fcertif = forms.DateField(label='Fecha Certificado',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	aus_fentrega_certif = forms.DateField(label='Fecha Entrega Certif.',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	aus_fcrondesde = forms.DateField(label='Fecha Desde',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	aus_fcronhasta = forms.DateField(label='Fecha Hasta',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	aus_freintegro = forms.DateField(label='Fecha Reintegro',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	aus_falta = forms.DateField(label='Fecha Alta',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	aus_frevision = forms.DateField(label=u'F.Prox.Revisión',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	art_fcontrol = forms.DateField(label='Fecha Control',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	art_faccidente = forms.DateField(label='Fecha Accidente',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	art_fdenuncia = forms.DateField(label='Fecha Denuncia',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))

	art_fcrondesde = forms.DateField(label='Fecha Desde',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	art_fcronhasta = forms.DateField(label='Fecha Hasta',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	art_freintegro = forms.DateField(label='Fecha Reintegro',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	art_falta = forms.DateField(label='Fecha Alta',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	art_frevision = forms.DateField(label=u'F.Próx.Revisión',required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))
	tipo_form = forms.CharField(widget = forms.HiddenInput(), required = False)	
	class Meta:
			model = ausentismo
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(AusentismoForm, self).__init__(*args, **kwargs)		
		self.fields['empleado'].queryset = ent_empleado.objects.filter(baja=False,empresa__pk__in=empresas_habilitadas(request))
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))				

	def clean(self):		
		super(forms.ModelForm,self).clean()	
		tipo_form = self.cleaned_data.get('tipo_form')
		
		empleado = self.cleaned_data.get('empleado')	
		if tipo_form=='ALTA':
			if not empleado:
					self.add_error("empleado",u'¡Debe cargar un Empleado!')

		aus_grupop = self.cleaned_data.get('aus_grupop')	
		if not aus_grupop:
				self.add_error("aus_grupop",u'¡Debe cargar un Grupo Patológico!')
		aus_diagn = self.cleaned_data.get('aus_diagn')	
		if not aus_diagn:
				self.add_error("aus_diagn",u'¡Debe cargar un Diagnóstico!')

		tipo_ausentismo = self.cleaned_data.get('tipo_ausentismo')	
		
		if int(tipo_ausentismo)== 1:
			aus_fcrondesde = self.cleaned_data.get('aus_fcrondesde')	
			aus_fcronhasta = self.cleaned_data.get('aus_fcronhasta')	
			aus_diascaidos= self.cleaned_data.get('aus_diascaidos')				
			if not aus_fcrondesde:
				self.add_error("aus_fcrondesde",u'¡Debe cargar una Fecha!')
			if not aus_fcronhasta:
				self.add_error("aus_fcronhasta",u'¡Debe cargar una Fecha!')
			if not aus_diascaidos:
				self.add_error("aus_diascaidos",u'¡Debe cargar un Día!')
			if aus_fcrondesde > aus_fcronhasta:
				self.add_error("aus_fcrondesde",u'¡Verifique las Fechas!')
		else:
			art_tipo_accidente = self.cleaned_data.get('art_tipo_accidente')							
			if not art_tipo_accidente:
				self.add_error("art_tipo_accidente",u'¡Debe seleccionar un Tipo de Accidente! Verifique.')
			else:
				art_faccidente = self.cleaned_data.get('art_faccidente')
				if not art_faccidente:
					self.add_error("art_faccidente",u'¡Debe cargar una Fecha!')
				art_fdenuncia = self.cleaned_data.get('art_fdenuncia')
				if not art_fdenuncia:
					self.add_error("art_fdenuncia",u'¡Debe cargar una Fecha!')					
				art_fcrondesde = self.cleaned_data.get('art_fcrondesde')	
				art_fcronhasta = self.cleaned_data.get('art_fcronhasta')	
				art_diascaidos= self.cleaned_data.get('art_diascaidos')	
				if not art_fcrondesde:
					self.add_error("art_fcrondesde",u'¡Debe cargar una Fecha!')
				if not art_fcronhasta:
					self.add_error("art_fcronhasta",u'¡Debe cargar una Fecha!')
				if not art_diascaidos:
					self.add_error("art_diascaidos",u'¡Debe cargar un Día!')
				if art_fcrondesde > art_fcronhasta:
					self.add_error("art_fcrondesde",u'¡Verifique las Fechas!')

		if self._errors:
			raise forms.ValidationError("¡Existen errores en la carga!.<br>Por favor verifique los campos marcados en rojo.")

		return self.cleaned_data

class ControlesDetalleForm(forms.ModelForm):	
	ausentismo = forms.IntegerField(widget = forms.HiddenInput(), required = False)
	detalle = forms.CharField(label='Detalle',widget=forms.Textarea(attrs={ 'class':'form-control','rows': 2}),required = False)				
	fecha = forms.DateField(required = False,widget=forms.DateInput(attrs={'class': 'datepicker'}))	
	class Meta:
			model = ausentismo_controles
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(ControlesDetalleForm, self).__init__(*args, **kwargs)



class ConsultaAusentismos(forms.Form):               	
	fdesde =  forms.DateField(label='Fecha Desde',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = False,initial=hoy())
	fhasta =  forms.DateField(label='Fecha Hasta',widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),required = False,initial=finMes())    	
	empresa = forms.ModelChoiceField(label='Empresa',queryset=ent_empresa.objects.filter(baja=False),empty_label='Todas',required=False)
	empleado = forms.CharField(required=False,label='Empleado')	
	tipo_ausentismo = forms.ChoiceField(label='Tipo Ausentismo',choices=TIPO_AUSENCIA_,required=False,initial=0)	
	estado = forms.ChoiceField(label='Vigencia',choices=TIPO_VIGENCIA,required=False,initial=0)	
	def __init__(self, *args, **kwargs):		
		request = kwargs.pop('request', None) 
		super(ConsultaAusentismos, self).__init__(*args, **kwargs)			
		self.fields['empresa'].queryset = ent_empresa.objects.filter(baja=False,pk__in=empresas_habilitadas(request))