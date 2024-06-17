# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput, NumberInput, Select
from entidades.models import ent_empleado, ent_medico_prof, ent_empresa_agrupamiento, ent_empresa
from .models import *
from laboralsalud.utilidades import *
from usuarios.views import tiene_permiso


class MedicoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_medico()


class PatologiaForm(forms.ModelForm):
    patologia = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": "autofocus"}), required=True
    )
    codigo = forms.CharField(required=False)

    class Meta:
        model = aus_patologia
        exclude = ["id", "baja"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(PatologiaForm, self).__init__(*args, **kwargs)


class DiagnosticoForm(forms.ModelForm):
    diagnostico = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": "autofocus"}), required=True
    )
    codigo = forms.CharField(required=False)

    class Meta:
        model = aus_diagnostico
        exclude = ["id", "baja"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(DiagnosticoForm, self).__init__(*args, **kwargs)

SINO_CHOICES = tuple([(None, '')] + list(SINO))

class AusentismoForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(
        label="Empleado",
        queryset=ent_empleado.objects.filter(baja=False),
        empty_label="---",
        required=True,
    )
    tipo_ausentismo = forms.ChoiceField(
        label="Tipo Ausentismo", choices=TIPO_AUSENCIA, required=False, initial=1
    )
    aus_tipo_alta = forms.ChoiceField(choices=TIPO_ALTA, required=True, initial=0)

    observaciones = forms.CharField(
        label=u"Recordatorio Médicos/Información Adicional",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 3}),
        required=False,
    )
    descr_altaparc = forms.CharField(
        label=u"Características de Alta con Restricción",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 2}),
        required=False,
    )
    detalle_acc_art = forms.CharField(
        label="Detalle Accidente ART",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 3}),
        required=False,
    )
    estudios_partic = forms.CharField(
        label=u"Estudios Particulares",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 2}),
        required=False,
    )
    estudios_art = forms.CharField(
        label="Estudios ART",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 2}),
        required=False,
    )
    recalificac_art = forms.CharField(
        label=u"Recalificación ART",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 2}),
        required=False,
    )
    aus_corta_certificado = forms.ChoiceField(
        label=u"Corta Certificado",
        choices=SINO_CHOICES,
        required=False,
        initial=None,
    )
    aus_grupop = forms.ModelChoiceField(
        label=agregar_nuevo_html(
            u"Grupo Patológico",
            "nuevoGrupoP",
            u"AGREGAR PATOLOGÍA",
            "/ausentismos/patologia/nuevo/",
            "recargarGP",
            u"Crear nueva Patología",
            "icon-magnifier-add",
        ),
        queryset=aus_patologia.objects.filter(baja=False),
        required=False,
    )
    aus_diagn = forms.ModelChoiceField(
        label=agregar_nuevo_html(
            u"Diagnóstico",
            "nuevoDiagn",
            u"AGREGAR DIAGNÓSTICO",
            "/ausentismos/diagnostico/nuevo/",
            "recargarD",
            u"Crear nuevo Diagnóstico",
            "icon-magnifier-add",
        ),
        queryset=aus_diagnostico.objects.filter(baja=False),
        required=False,
    )
    aus_medico = MedicoModelChoiceField(
        label=agregar_nuevo_html(
            u"Médico Tratante/ART",
            "nuevoMedicoAUS",
            u"AGREGAR MÉDICO",
            "/entidades/medico_prof/nuevo/",
            "recargarM",
            u"Crear nuevo Médico",
            "icon-users",
        ),
        queryset=ent_medico_prof.objects.filter(baja=False).select_related(
            "especialidad"
        ),
        required=False,
    )
    empresa = forms.ModelChoiceField(
        label="Empresa", queryset=ent_empresa.objects.filter(baja=False), required=False
    )
    aus_fcontrol = forms.DateField(
        label=popover_html(
            u"Fecha Próx.Control", u"Actualizar a Fecha de próximo Control Programado"
        ),
        required=False,
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    aus_fcrondesde = forms.DateField(
        label="Fecha Desde",
        required=False,
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    aus_fcronhasta = forms.DateField(
        label="Fecha Hasta",
        required=False,
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    aus_freintegro = forms.DateField(
        label="Fecha Reintegro",
        required=False,
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    aus_falta = forms.DateField(
        label="Fecha Alta",
        required=False,
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    art_faccidente = forms.DateField(
        label="Fecha Accidente",
        required=False,
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    art_fdenuncia = forms.DateField(
        label="Fecha Denuncia",
        required=False,
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )

    plan_accion = forms.CharField(
        label=u"Detalle del Plan de Acción",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 10}),
        required=False,
    )

    tipo_form = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ausentismo
        exclude = ["id", "fecha_creacion", "fecha_modif", "usuario_carga", "aus_certificado", "aus_control"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        tipo_form = kwargs.pop("tipo_form", None)
        ausentismo = kwargs.pop("ausentismo", None)
        super(AusentismoForm, self).__init__(*args, **kwargs)
        empresas = empresas_habilitadas(request)
        if tipo_form == "EDICION":
            self.fields["empleado"].queryset = ent_empleado.objects.filter(pk=ausentismo.empleado.pk)
        else:
            # self.fields["empleado"].queryset = ent_empleado.objects.filter(baja=False, empresa__pk__in=empresas)
            # self.fields["empleado"].queryset = ent_empleado.objects.none()
            self.fields["empresa"].queryset = ent_empresa.objects.filter(
                baja=False, pk__in=empresas
            )
            self.fields["empleado"].label = agregar_nuevo_html(
                label="Empleado",
                id="nuevoEmpleado",
                title="AGREGAR EMPLEADO",
                url="/entidades/empleado/nuevo/",
                callback="recargarE",
                hint="Crear Nuevo Empleado",
                icon="icon-users",
            )


        usuario = usuario_actual(request)
        # Si es médico no vé los últimos tipos
        if usuario.tipoUsr > 1:
            self.fields["tipo_ausentismo"].choices = TIPO_AUSENCIA

        if not tiene_permiso(request, "pat_pantalla"):
            self.fields["aus_grupop"].queryset = aus_patologia.objects.filter(
                baja=False
            )
            self.fields["aus_grupop"].label = u"Grupo Patológico"
        if not tiene_permiso(request, "diag_pantalla"):
            self.fields["aus_diagn"].queryset = aus_diagnostico.objects.filter(
                baja=False
            )
            self.fields["aus_diagn"].label = u"Diagnóstico"
        if not tiene_permiso(request, "med_pantalla"):
            self.fields["aus_medico"].queryset = ent_medico_prof.objects.filter(
                baja=False
            )
            self.fields["aus_medico"].label = u"Médico Tratante/ART"

    def clean(self):
        super(forms.ModelForm, self).clean()
        tipo_form = self.cleaned_data.get("tipo_form")
        empleado = self.cleaned_data.get("empleado")
        if not empleado:
            raise forms.ValidationError("Debe cargar un Empleado!")

        tipo_ausentismo = self.cleaned_data.get("tipo_ausentismo")
        aus_fcrondesde = self.cleaned_data.get("aus_fcrondesde")
        aus_fcronhasta = self.cleaned_data.get("aus_fcronhasta")
        aus_diascaidos = self.cleaned_data.get("aus_diascaidos")

        if not aus_fcrondesde:
            self.add_error("aus_fcrondesde", u"¡Debe cargar una Fecha!")
        if not aus_fcronhasta:
            self.add_error("aus_fcronhasta", u"¡Debe cargar una Fecha!")
        # Si es un control no exijo los dias caidos ni control de fechas
        if int(tipo_ausentismo) == 8:
            self.cleaned_data["aus_diascaidos"] = 0
        else:
            aus_grupop = self.cleaned_data.get("aus_grupop")
            if not aus_grupop:
                self.add_error("aus_grupop", u"¡Debe cargar un Grupo Patológico!")
            aus_diagn = self.cleaned_data.get("aus_diagn")
            if not aus_diagn:
                self.add_error("aus_diagn", u"¡Debe cargar un Diagnóstico!")
            if not aus_diascaidos:
                self.add_error("aus_diascaidos", u"¡Debe cargar un Día!")

            if aus_fcrondesde and aus_fcronhasta:
                if aus_fcrondesde > aus_fcronhasta:
                    self.add_error("aus_fcrondesde", u"¡Verifique las Fechas!")

            aus_tipo_alta = self.cleaned_data.get("aus_tipo_alta")
            if not aus_tipo_alta:
                self.add_error(
                    "aus_tipo_alta", u"¡Debe seleccionar un Tipo de Alta! Verifique."
                )

            elif aus_tipo_alta == 2:
                descr_altaparc = self.cleaned_data.get("descr_altaparc")
                if not descr_altaparc:
                    self.add_error(
                        "descr_altaparc", u"¡Debe cargar el Detalle del Alta!"
                    )

            if int(tipo_ausentismo) not in (1, 4, 5, 6, 7):
                art_tipo_accidente = self.cleaned_data.get("art_tipo_accidente")
                if not art_tipo_accidente:
                    self.add_error(
                        "art_tipo_accidente",
                        u"¡Debe seleccionar un Tipo de Accidente! Verifique.",
                    )
                else:
                    art_faccidente = self.cleaned_data.get("art_faccidente")
                    if not art_faccidente:
                        self.add_error("art_faccidente", u"¡Debe cargar una Fecha!")
                    art_fdenuncia = self.cleaned_data.get("art_fdenuncia")
                    if not art_fdenuncia:
                        self.add_error("art_fdenuncia", u"¡Debe cargar una Fecha!")

        if self._errors:
            raise forms.ValidationError(
                "¡Existen errores en la carga!.<br>Verifique los campos marcados en rojo."
            )

        return self.cleaned_data


class ControlesDetalleForm(forms.ModelForm):
    detalle = forms.CharField(
        label="Detalles/Observaciones",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 3}),
        required=False,
    )
    fecha = forms.DateField(
        label=popover_html(
            label=u"Fecha Control",
            content=u"Fechas/Historial de Control (ascendente)",
            placement="right",
        ),
        required=False,
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
    )
    tipo_control = forms.ChoiceField(
        label="Tipo Control", choices=TIPO_CONTROL, required=False,
    )
    # aus_fcrondesde = forms.DateField(
    #     label="Certificado Desde",
    #     required=False,
    #     widget=forms.DateInput(attrs={"class": "datepicker"}),
    # )
    # aus_fcronhasta = forms.DateField(
    #     label="Certificado Hasta",
    #     required=False,
    #     widget=forms.DateInput(attrs={"class": "datepicker"}),
    # )

    class Meta:
        model = ausentismo_controles
        exclude = ["id", "ausentismo", "fecha_creacion", "fecha_modif", "usuario_carga"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ControlesDetalleForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

    def clean(self):
        tipo_control = self.cleaned_data.get("tipo_control")
        fecha = self.cleaned_data.get("fecha")

        if fecha:
            if not tipo_control:
                self.add_error("tipo_control", u"¡Debe cargar una Tipo de Control!")

            # aus_fcrondesde = self.cleaned_data.get("aus_fcrondesde")
            # aus_fcronhasta = self.cleaned_data.get("aus_fcronhasta")
            #
            # if aus_fcrondesde:
            #     if not aus_fcronhasta:
            #         self.add_error("aus_fcronhasta", u"¡Verifique la Fecha!")
            #     elif aus_fcrondesde > aus_fcronhasta:
            #         self.add_error("aus_fcronhasta", u"¡Verifique la Fechas!")

        return self.cleaned_data


class PatologiaDetalleForm(forms.ModelForm):
    ausentismo = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    detalle = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 3}),
        required=False,
    )
    fecha = forms.DateField(
        label="",
        required=False,
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
    )

    class Meta:
        model = ausentismo_controles_patologias
        exclude = ["id", "fecha_creacion", "fecha_modif", "usuario_carga"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(PatologiaDetalleForm, self).__init__(*args, **kwargs)


class ConsultaAusentismos(forms.Form):
    fcontrol = forms.DateField(
        label="F.Próx.Control",
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
        required=False,
    )
    fdesde = forms.DateField(
        label="F.Cron.Desde",
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
        initial=ultimo_anio(),
        required=False,
    )
    fhasta = forms.DateField(
        label="F.Cron.Hasta",
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
        initial=fin_de_los_tiempos(),
        required=False,
    )
    empresa = forms.ModelChoiceField(
        label="Empresa",
        queryset=ent_empresa.objects.filter(baja=False),
        empty_label="Todas",
        required=False,
    )
    empleado = forms.CharField(required=False, label="Empleado")
    aus_grupop = forms.CharField(label=u"Grupo Patológico", required=False)
    aus_diagn = forms.CharField(label=u"Diagnóstico", required=False)
    tipo_ausentismo = forms.ChoiceField(
        label="Tipo Ausentismo", choices=TIPO_AUSENCIA_, required=False, initial=0
    )
    estado = forms.ChoiceField(
        label="Vigencia", choices=TIPO_VIGENCIA, required=False, initial=0
    )
    agrupamiento = forms.ModelChoiceField(
        label="Agrupamiento/Gerencia",
        queryset=ent_empresa_agrupamiento.objects.filter(baja=False),
        initial=0,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        empresas = kwargs.pop("empresas", [])
        super(ConsultaAusentismos, self).__init__(*args, **kwargs)
        self.fields["empresa"].queryset = ent_empresa.objects.filter(
            baja=False, pk__in=empresas
        )


class ImportarAusentismosForm(forms.Form):
    empresa = forms.ModelChoiceField(
        label="Empresa",
        queryset=ent_empresa.objects.filter(baja=False),
        empty_label="----",
        required=True,
    )
    archivo = forms.FileField(label="Seleccione un archivo", required=True)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ImportarAusentismosForm, self).__init__(*args, **kwargs)
        self.fields["empresa"].queryset = ent_empresa.objects.filter(
            baja=False, pk__in=empresas_habilitadas(request)
        )

    def clean(self):
        archivo = self.cleaned_data.get("archivo")
        if archivo:
            if not archivo.name.endswith(".csv"):
                self.add_error("archivo", u"¡El archivo debe tener extensión .CSV!")
            # if file is too large, return
            if archivo.multiple_chunks():
                self.add_error(
                    "archivo",
                    u"El archivo es demasiado grande (%.2f MB)."
                    % (archivo.size / (1000 * 1000),),
                )
        return self.cleaned_data


ACCIONES = (
    (1, u"Enviar por e-mail"),
    (2, u"Sólo Generar"),
)


class InformeAusenciasForm(forms.Form):
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
        required=True,
        initial=hoy(),
    )
    asunto = forms.CharField(required=False, label="Asunto")
    destinatario = forms.EmailField(
        max_length=50, label="E-Mail Destinatario/s", required=True
    )
    observaciones = forms.CharField(
        label="Observaciones Informe",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 5}),
        required=False,
    )
    ausentismo_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(InformeAusenciasForm, self).__init__(*args, **kwargs)

    def clean(self):
        fecha = self.cleaned_data.get("fecha")
        destinatario = self.cleaned_data.get("destinatario")
        if not fecha:
            self.add_error("fecha", u"¡Debe cargar una Fecha!")
        if not destinatario:
            self.add_error("destinatario", u"¡Debe cargar un Email de Destino válido!")

        return self.cleaned_data


class ImprimirInformeAusenciasForm(forms.Form):
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
        required=True,
        initial=hoy(),
    )
    observaciones = forms.CharField(
        label="Observaciones Informe",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 9}),
        required=False,
    )
    lista = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ImprimirInformeAusenciasForm, self).__init__(*args, **kwargs)


class SeguimControlForm(forms.ModelForm):
    detalle = forms.CharField(
        label="Detalles/Observaciones",
        widget=forms.Textarea(attrs={"class": "form-control2", "rows": 5}),
        required=True,
    )
    fecha = forms.DateField(
        label="Fecha Control",
        required=True,
        initial=hoy(),
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "autocomplete": "off"}
        ),
    )
    tipo_control = forms.ChoiceField(
        label="Tipo Control", choices=TIPO_CONTROL, required=False,
    )

    class Meta:
        model = ausentismo_controles
        exclude = ["id", "fecha_creacion", "fecha_modif", "usuario_carga"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(SeguimControlForm, self).__init__(*args, **kwargs)

    def clean(self):
        tipo_control = self.cleaned_data.get("tipo_control")
        fecha = self.cleaned_data.get("fecha")
        if fecha:
            if not tipo_control:
                self.add_error("tipo_control", u"¡Debe cargar una Tipo de Control!")
        return self.cleaned_data
