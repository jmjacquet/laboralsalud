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
	tipo_ausentismo = forms.ChoiceField(label='',choices=TIPO_AUSENCIA,required=True,initial=1)
	class Meta:
			model = ausentismo
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(AusentismoForm, self).__init__(*args, **kwargs)		
	