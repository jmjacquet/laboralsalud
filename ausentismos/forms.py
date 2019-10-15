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
	empleado = EntidadModelChoiceField(label='',queryset=ent_empleado.objects.filter(baja=False),empty_label='---',required = False)	
	# apellido_y_nombre = forms.CharField(label='',widget=forms.TextInput(attrs={ 'class':'form-control','readonly': 'readonly'}),required = False)				
	# nro_doc = forms.IntegerField(label='',widget=forms.TextInput(attrs={ 'class':'form-control','readonly': 'readonly'}),required = False)
	# legajo = forms.IntegerField(label='',widget=forms.TextInput(attrs={ 'class':'form-control','readonly': 'readonly'}),required = False)
	tipo_ausentismo = forms.ChoiceField(label='',choices=TIPO_AUSENCIA,required=False,initial=1)
	aus_control = forms.ChoiceField(label=u'¿Asistió a Control?',choices=SINO,required=False,initial='N')
	aus_certificado = forms.ChoiceField(label=u'¿Presenta Certificado?',choices=SINO,required=False,initial='N')
	aus_diagn = forms.CharField(label='Diagnóstico',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	observaciones = forms.CharField(label='Observaciones',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	descr_altaparc = forms.CharField(label=u'Descripción Alta Parcial',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	detalle_acc_art = forms.CharField(label='Detalle Accidente ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	estudios_partic = forms.CharField(label=u'Estudios Particulares',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	estudios_art = forms.CharField(label='Estudios ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	recalificac_art = forms.CharField(label=u'Recalificación ART',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 2}),required = False)	
	class Meta:
			model = ausentismo
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(AusentismoForm, self).__init__(*args, **kwargs)		
	