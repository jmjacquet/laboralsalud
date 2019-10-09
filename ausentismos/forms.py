# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,NumberInput,Select
from .models import *

from laboralsalud.utilidades import *

class AusentismoForm(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),required=True)	
	
	class Meta:
			model = ausentismo
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(AusentismoForm, self).__init__(*args, **kwargs)		