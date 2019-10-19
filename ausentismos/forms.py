# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import *
from entidades.models import ent_empleado
from laboralsalud.utilidades import *


class EntidadModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return obj.get_empleado()


class AusentismoForm(forms.ModelForm):
	empleado = EntidadModelChoiceField(label='',queryset=ent_empleado.objects.filter(baja=False),empty_label='---',required = True)	
	# apellido_y_nombre = forms.CharField(label='',widget=forms.TextInput(attrs={ 'class':'form-control','readonly': 'readonly'}),required = False)				
	# nro_doc = forms.IntegerField(label='',widget=forms.TextInput(attrs={ 'class':'form-control','readonly': 'readonly'}),required = False)
	# legajo = forms.IntegerField(label='',widget=forms.TextInput(attrs={ 'class':'form-control','readonly': 'readonly'}),required = False)
	tipo_ausentismo = forms.ChoiceField(label='',choices=TIPO_AUSENCIA,required=False,initial=1)
	aus_control = forms.ChoiceField(label=u'¿Asistió a Control?',choices=SINO,required=False,initial='N')
	aus_certificado = forms.ChoiceField(label=u'¿Presenta Certificado?',choices=SINO,required=False,initial='N')
	observaciones = forms.CharField(label='Observaciones',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	descr_altaparc = forms.CharField(label=u'Descripción Alta Parcial',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	detalle_acc_art = forms.CharField(label='Detalle Accidente ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	estudios_partic = forms.CharField(label=u'Estudios Particulares',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	estudios_art = forms.CharField(label='Estudios ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	recalificac_art = forms.CharField(label=u'Recalificación ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	aus_grupop = forms.ModelChoiceField(label=u'Grupo Patológico',queryset=aus_patologia.objects.filter(baja=False),required=True)
	aus_diagn = forms.ModelChoiceField(label=u'Diagnóstico',queryset=aus_diagnostico.objects.filter(baja=False),required=True)
	class Meta:
			model = ausentismo
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(AusentismoForm, self).__init__(*args, **kwargs)		
		self.fields['empleado'].queryset = ent_empleado.objects.filter(empresa__pk__in=empresas_habilitadas(request))

	def clean(self):		
		super(forms.ModelForm,self).clean()	
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