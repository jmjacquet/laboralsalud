# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
import datetime

from ausentismos.models import aus_patologia
from laboralsalud.utilidades import *
from entidades.models import (
    ent_art,
    ent_cargo,
    ent_especialidad,
    ent_medico_prof,
    ent_empresa,
    ent_empleado,
    ent_empresa_agrupamiento,
)
from entidades.forms import TrabajoModelChoiceField


def mes_anio(fecha):
    return fecha.strftime("%m/%Y")


class ConsultaPeriodo(forms.Form):
    periodo = forms.DateField(
        label="Período",
        input_formats=["%m/%Y"],
        widget=forms.DateInput(attrs={"class": "form-control datepicker"}),
        required=True,
        initial=mes_anio(inicioMes()),
    )
    empresa = forms.ModelChoiceField(
        label="Empresa",
        queryset=ent_empresa.objects.filter(baja=False),
        initial=0,
        required=False,
    )
    agrupamiento = forms.ModelChoiceField(
        label="Agrupamiento/Gerencia",
        queryset=ent_empresa_agrupamiento.objects.filter(baja=False),
        initial=0,
        required=False,
    )
    grupo_patologico = forms.ModelChoiceField(
        label=u"Grupo Patológico",
        queryset=aus_patologia.objects.filter(baja=False),
        required=False,
    )
    empleado = forms.CharField(required=False, label="Empleado")
    tipo_ausentismo = forms.ChoiceField(
        label="Tipo Ausentismo", choices=TIPO_AUSENCIA_, required=False, initial=0
    )
    trab_cargo = TrabajoModelChoiceField(
        label=u"Puesto de Trabajo",
        queryset=ent_cargo.objects.filter(baja=False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ConsultaPeriodo, self).__init__(*args, **kwargs)
        self.fields["empresa"].queryset = ent_empresa.objects.filter(
            baja=False, pk__in=empresas_habilitadas(request)
        )

    def clean(self):
        agrupamiento = self.cleaned_data.get("agrupamiento")
        empresa = self.cleaned_data.get("empresa")
        if not empresa and not agrupamiento:
            raise forms.ValidationError("¡Debe seleccionar un Agrupamiento/Gerencia y/o una Empresa!")


class ConsultaAnual(forms.Form):
    periodo_desde = forms.DateField(
        label="Período Desde",
        input_formats=["%m/%Y"],
        widget=forms.DateInput(attrs={"class": "form-control datepicker"}),
        required=True,
        initial=mes_anio(inicioAnio()),
    )
    periodo_hasta = forms.DateField(
        label="Período Hasta",
        input_formats=["%m/%Y"],
        widget=forms.DateInput(attrs={"class": "form-control datepicker"}),
        required=True,
        initial=mes_anio(finMes()),
    )
    empresa = forms.ModelChoiceField(
        label="Empresa",
        queryset=ent_empresa.objects.filter(baja=False),
        required=False,
        initial=0,
    )
    empleado = forms.CharField(required=False, label="Empleado")
    tipo_ausentismo = forms.ChoiceField(
        label="Tipo Ausentismo", choices=TIPO_AUSENCIA_, required=False, initial=0
    )
    trab_cargo = TrabajoModelChoiceField(
        label=u"Puesto de Trabajo",
        queryset=ent_cargo.objects.filter(baja=False),
        required=False,
    )
    agrupamiento = forms.ModelChoiceField(
        label="Agrupamiento/Gerencia",
        queryset=ent_empresa_agrupamiento.objects.filter(baja=False),
        initial=0,
        required=False,
    )
    grupo_patologico = forms.ModelChoiceField(
        label=u"Grupo Patológico",
        queryset=aus_patologia.objects.filter(baja=False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ConsultaAnual, self).__init__(*args, **kwargs)
        self.fields["empresa"].queryset = ent_empresa.objects.filter(
            baja=False, pk__in=empresas_habilitadas(request)
        )

    def clean(self):
        agrupamiento = self.cleaned_data.get("agrupamiento")
        empresa = self.cleaned_data.get("empresa")
        if not empresa and not agrupamiento:
            raise forms.ValidationError("¡Debe seleccionar un Agrupamiento/Gerencia y/o una Empresa!")

