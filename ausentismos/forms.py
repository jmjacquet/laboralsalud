# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import *
from entidades.models import ent_empleado
from chosen import forms as chosenforms
from laboralsalud.utilidades import *


class EntidadModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):		
		return obj.get_empleado()


class AusentismoForm(forms.ModelForm):
	empleado = EntidadModelChoiceField(label='Empleado',queryset=ent_empleado.objects.filter(baja=False),empty_label='---',required = False)
	
	
	class Meta:
			model = ausentismo
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(AusentismoForm, self).__init__(*args, **kwargs)		