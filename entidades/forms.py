# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import ent_art

class ARTForm(forms.ModelForm):
	# observaciones = forms.CharField(label='Observaciones / Datos adicionales',widget=forms.Textarea(attrs={'class':'form-control2', 'rows': 5}),required = False)	
	# fact_cuit = ARCUITField(label='CUIT',required = False,widget=PostPendWidgetBuscar(attrs={'class':'form-control','autofocus':'autofocus'},
	# 		base_widget=TextInput,data='<i class="fa fa-search" aria-hidden="true"></i>',tooltip=u"Buscar datos y validar CUIT en AFIP"))		
	# fact_categFiscal = forms.ChoiceField(label=u'Categoría Fiscal',required = True,choices=CATEG_FISCAL,initial=5)	
	# fact_nro_doc = ARDNIField(label=u'Número',required = False)	
	# tipo_doc = forms.ChoiceField(label=u'Tipo Documento',required = True,choices=TIPO_DOC)
	# cod_postal = ARPostalCodeField(label='CP',required = False)		
	# tipo_entidad = forms.IntegerField(widget = forms.HiddenInput(), required = False)
	# empresa = forms.ModelChoiceField(queryset=gral_empresa.objects.all(),empty_label=None)
	# dcto_general = forms.DecimalField(label=u'% Dcto.General',initial=0,decimal_places=2,required = False)	
	# tope_cta_cte = forms.DecimalField(widget=PrependWidget(attrs={'class':'form-control','step':0.00},base_widget=NumberInput, data='$'),initial=0.00,decimal_places=2,required = False)
	# lista_precios_defecto = forms.ModelChoiceField(label=u'Lista Precios x Defecto',queryset=prod_lista_precios.objects.all(),required = False)
	class Meta:
			model = ent_art
			exclude = ['id','fecha_creacion','fecha_modif','usuario_carga']

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super(ARTForm, self).__init__(*args, **kwargs)
		# self.fields['lista_precios_defecto'].queryset = prod_lista_precios.objects.filter(baja=False,empresa__id__in=empresas_habilitadas(request))		
		# try:
		# 	empresas = empresas_buscador(request)			
		# 	self.fields['empresa'].queryset = empresas
		# 	self.fields['empresa'].initial = 1
		# except:
		# 	empresas = empresa_actual(request)  
		# 	self.fields['empresa'].queryset = empresas		
			

	# def clean(self):		
	# 	fact_cuit = self.cleaned_data.get('fact_cuit')
	# 	tipo_entidad = self.cleaned_data.get('tipo_entidad')
	# 	fact_categFiscal = self.cleaned_data.get('fact_categFiscal')
	# 	tipo_doc = self.cleaned_data.get('tipo_doc')
	# 	if fact_cuit: 
	# 		try:
	# 			entidad=egr_entidad.objects.filter(fact_cuit=fact_cuit,tipo_entidad=tipo_entidad,baja=False)				
	# 			if entidad:
	# 				raise forms.ValidationError("El Nº de CUIT ingresado ya existe en el Sistema! Verifique.")
	# 		except egr_entidad.DoesNotExist:
	# 		#because we didn't get a match
	# 			pass

	# 	if fact_categFiscal and tipo_doc:
	# 		if (int(fact_categFiscal)==1)and(int(tipo_doc)==80)and(not validar_cuit(fact_cuit)):
	# 			raise forms.ValidationError(u'Debe cargar un CUIT válido! Verifique.')

	# 		if (int(fact_categFiscal)==1)and(int(tipo_doc)!=80):
	# 			raise forms.ValidationError(u'Si es IVA R.I. debe seleccionar CUIT como tipo de Documento! Verifique.')				


	# 	return self.cleaned_data
