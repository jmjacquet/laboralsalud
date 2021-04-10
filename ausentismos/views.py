# -*- coding: utf8 -*-
from __future__ import unicode_literals
import io
import csv
from easy_pdf.rendering import render_to_pdf_response, render_to_pdf
from django.template.loader import get_template
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail, EmailMessage
import random
import datetime
from general.views import getVariablesMixin
from .forms import ImportarAusentismosForm, InformeAusenciasForm, ImprimirInformeAusenciasForm
from django.shortcuts import render
from django.template import RequestContext, Context
from django.shortcuts import *
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView, DetailView
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib import messages
from laboralsalud.utilidades import ultimoNroId, usuario_actual
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from modal.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from django.db.models import Q, Sum, Count, FloatField, Func
from django.forms.models import inlineformset_factory, BaseInlineFormSet, formset_factory
from django.utils.functional import curry
from django.http import FileResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_protect


from .models import *
from entidades.models import ent_empleado
from general.views import VariablesMixin
from usuarios.views import tiene_permiso
from .forms import (
    AusentismoForm,
    PatologiaForm,
    DiagnosticoForm,
    ConsultaAusentismos,
    ControlesDetalleForm,
    PatologiaDetalleForm,
    SeguimControlForm,
)
from general.models import configuracion

############ AUSENTISMOS ############################


class AusentismoView(VariablesMixin, ListView):
    model = ausentismo
    template_name = "ausentismos/ausentismo_listado.html"
    context_object_name = "ausentismos"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "aus_pantalla"):
            return redirect(reverse("principal"))
        return super(AusentismoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AusentismoView, self).get_context_data(**kwargs)
        busq = None
        if self.request.POST:
            busq = self.request.POST
        else:
            if "ausentismos" in self.request.session:
                busq = self.request.session["ausentismos"]
        form = ConsultaAusentismos(busq or None, request=self.request)
        fdesde = hoy()
        fhasta = finMes()
        empresas = empresas_habilitadas(self.request)
        ausentismos = ausentismo.objects.filter(
            baja=False, empleado__empresa__pk__in=empresas, aus_fcronhasta__gte=hoy()
        )
        if form.is_valid():
            fcontrol = form.cleaned_data["fcontrol"]
            fdesde = form.cleaned_data["fdesde"]
            fhasta = form.cleaned_data["fhasta"]
            empresa = form.cleaned_data["empresa"]
            empleado = form.cleaned_data["empleado"]
            aus_grupop = form.cleaned_data["aus_grupop"]
            aus_diagn = form.cleaned_data["aus_diagn"]
            tipo_ausentismo = form.cleaned_data["tipo_ausentismo"]
            estado = form.cleaned_data["estado"]
            if not fdesde:
                fdesde = ultimo_anio()
            if not fhasta:
                fhasta = proximo_anio()

            ausentismos = ausentismo.objects.filter(empleado__empresa__pk__in=empresas)

            if int(estado) == 1:
                ausentismos = ausentismos.filter(aus_fcronhasta__gte=hoy())
            elif int(estado) == 2:
                ausentismos = ausentismos.filter(aus_fcronhasta__lt=hoy())
            elif int(estado) == 0:
                ausentismos = ausentismos.filter(
                    Q(aus_fcrondesde__range=[fdesde, fhasta])
                    | Q(aus_fcronhasta__range=[fdesde, fhasta])
                    | Q(aus_fcrondesde__lt=fdesde, aus_fcronhasta__gt=fhasta)
                )
            if empresa:
                ausentismos = ausentismos.filter(
                    Q(empleado__empresa=empresa) | Q(empleado__empresa__casa_central=empresa)
                )
            if empleado:
                ausentismos = ausentismos.filter(
                    Q(empleado__apellido_y_nombre__icontains=empleado) | Q(empleado__nro_doc__icontains=empleado)
                )
            if fcontrol:
                ausentismos = ausentismos.filter(aus_fcontrol=fcontrol)
            if int(tipo_ausentismo) > 0:
                if int(tipo_ausentismo) == 11:
                    ausentismos = ausentismos.filter(Q(aus_diascaidos__lte=30) | Q(art_diascaidos__lte=30))
                elif int(tipo_ausentismo) == 12:
                    ausentismos = ausentismos.filter(Q(aus_diascaidos__gt=30) | Q(art_diascaidos__gt=30))
                else:
                    ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))
            if aus_grupop:
                ausentismos = ausentismos.filter(aus_grupop__patologia__icontains=aus_grupop)
            if aus_diagn:
                ausentismos = ausentismos.filter(aus_diagn__diagnostico__icontains=aus_diagn)

            self.request.session["ausentismos"] = self.request.POST
        else:
            self.request.session["ausentismos"] = None
        context["form"] = form
        context["ausentismos"] = ausentismos.select_related(
            "empleado", "empleado__empresa", "aus_grupop", "aus_diagn", "usuario_carga"
        )
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class ControlesDetalleFormSet(BaseInlineFormSet):
    pass


ControlDetalleFormSet = inlineformset_factory(
    ausentismo,
    ausentismo_controles,
    form=ControlesDetalleForm,
    formset=ControlesDetalleFormSet,
    can_delete=True,
    extra=0,
    min_num=100,
)


class PatologiasDetalleFormSet(BaseInlineFormSet):
    pass


PatologiaDetalleFormSet = inlineformset_factory(
    ausentismo,
    ausentismo_controles_patologias,
    form=PatologiaDetalleForm,
    formset=PatologiasDetalleFormSet,
    can_delete=True,
    extra=0,
    min_num=100,
)


class AusentismoCreateView(VariablesMixin, CreateView):
    form_class = AusentismoForm
    template_name = "ausentismos/ausentismo_form.html"
    model = ausentismo

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "aus_abm"):
            return redirect(reverse("principal"))
        return super(AusentismoCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields["empleado"].label = agregar_nuevo_html(
            "Empleado",
            "nuevoEmpleado",
            "AGREGAR EMPLEADO",
            "/entidades/empleado/nuevo/",
            "recargarE",
            "Crear Nuevo Empleado",
            "icon-users",
        )
        controles_detalle = ControlDetalleFormSet(prefix="formDetalle")
        controles_patologias = PatologiaDetalleFormSet(prefix="formDetalle2")
        return self.render_to_response(
            self.get_context_data(
                form=form, controles_detalle=controles_detalle, controles_patologias=controles_patologias
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        controles_detalle = ControlDetalleFormSet(self.request.POST, instance=self.object, prefix="formDetalle")
        controles_patologias = PatologiaDetalleFormSet(self.request.POST, instance=self.object, prefix="formDetalle2")
        if form.is_valid() and controles_detalle.is_valid() and controles_patologias.is_valid():
            return self.form_valid(form, controles_detalle, controles_patologias)
        else:
            return self.form_invalid(form, controles_detalle, controles_patologias)

    def form_valid(self, form, controles_detalle, controles_patologias):
        self.object = form.save(commit=False)
        self.object.usuario_carga = usuario_actual(self.request)
        self.object.save()
        controles_detalle.instance = self.object
        controles_detalle.ausentismo = self.object.id
        controles_detalle.usuario_carga = usuario_actual(self.request)
        controles_detalle.save()
        controles_patologias.instance = self.object
        controles_patologias.ausentismo = self.object.id
        controles_patologias.usuario_carga = usuario_actual(self.request)
        controles_patologias.save()
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return HttpResponseRedirect(reverse("ausentismo_listado"))

    def form_invalid(self, form, controles_detalle, controles_patologias):
        return self.render_to_response(
            self.get_context_data(
                form=form, controles_detalle=controles_detalle, controles_patologias=controles_patologias
            )
        )

    def get_form_kwargs(self):
        kwargs = super(AusentismoCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(AusentismoCreateView, self).get_initial()
        initial["request"] = self.request
        initial["tipo_form"] = "ALTA"
        return initial

    def get_success_url(self):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return reverse("ausentismo_listado")


class AusentismoEditView(VariablesMixin, UpdateView):
    form_class = AusentismoForm
    model = ausentismo
    pk_url_kwarg = "id"
    template_name = "ausentismos/ausentismo_form.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "aus_abm"):
            return redirect(reverse("principal"))
        return super(AusentismoEditView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields["empleado"].widget.attrs["disabled"] = True
        controles_detalle = ControlDetalleFormSet(instance=self.object, prefix="formDetalle")
        controles_patologias = PatologiaDetalleFormSet(instance=self.object, prefix="formDetalle2")
        return self.render_to_response(
            self.get_context_data(
                form=form, controles_detalle=controles_detalle, controles_patologias=controles_patologias
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        controles_detalle = ControlDetalleFormSet(self.request.POST, instance=self.object, prefix="formDetalle")
        controles_patologias = PatologiaDetalleFormSet(self.request.POST, instance=self.object, prefix="formDetalle2")
        if form.is_valid() and controles_detalle.is_valid() and controles_patologias.is_valid():
            return self.form_valid(form, controles_detalle, controles_patologias)
        else:
            return self.form_invalid(form, controles_detalle, controles_patologias)

    def form_valid(self, form, controles_detalle, controles_patologias):
        self.object.save()
        controles_detalle.instance = self.object
        controles_detalle.ausentismo = self.object.id
        controles_detalle.save()
        controles_patologias.instance = self.object
        controles_patologias.ausentismo = self.object.id
        controles_patologias.usuario_carga = usuario_actual(self.request)
        controles_patologias.save()
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return HttpResponseRedirect(reverse("ausentismo_listado"))

    def form_invalid(self, form, controles_detalle, controles_patologias):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields["empleado"].widget.attrs["disabled"] = True
        return self.render_to_response(
            self.get_context_data(
                form=form, controles_detalle=controles_detalle, controles_patologias=controles_patologias
            )
        )

    def get_form_kwargs(self):
        kwargs = super(AusentismoEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(AusentismoEditView, self).get_initial()
        initial["request"] = self.request
        initial["tipo_form"] = "EDICION"
        return initial

    def get_success_url(self):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return reverse("ausentismo_listado")


class AusentismoVerView(VariablesMixin, DetailView):
    model = ausentismo
    pk_url_kwarg = "id"
    context_object_name = "a"
    template_name = "ausentismos/ausentismo_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AusentismoVerView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AusentismoVerView, self).get_context_data(**kwargs)
        a = self.get_object()
        context["controles"] = ausentismo_controles.objects.filter(ausentismo=a).exclude(
            Q(fecha__isnull=True, detalle__isnull=True) | Q(fecha__isnull=True, detalle="")
        )
        context["controles_pat"] = ausentismo_controles_patologias.objects.filter(ausentismo=a).exclude(
            Q(fecha__isnull=True, detalle__isnull=True) | Q(fecha__isnull=True, detalle="")
        )
        return context


class AusentismoHistorialView(VariablesMixin, DetailView):
    model = ent_empleado
    pk_url_kwarg = "id"
    context_object_name = "empleado"
    template_name = "ausentismos/historia_clinica.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AusentismoHistorialView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AusentismoHistorialView, self).get_context_data(**kwargs)
        e = self.get_object()
        context["historial"] = ausentismo.objects.filter(empleado=e)
        return context


class SeguimControlCreateView(VariablesMixin, AjaxCreateView):
    form_class = SeguimControlForm
    template_name = "modal/ausentismos/form_control.html"
    pk_url_kwarg = "id"
    model = ausentismo_controles

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "aus_abm"):
            return redirect(reverse("ausentismo_listado"))
        return super(SeguimControlCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        aus = self.get_object()
        self.object.ausentismo = aus
        self.object.usuario_carga = usuario_actual(self.request)
        self.object.save()
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(SeguimControlCreateView, self).form_valid(form)

    def get_object(self):
        return get_object_or_404(ausentismo, pk=self.kwargs.get("id", None))

    def get_form_kwargs(self):
        kwargs = super(SeguimControlCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(SeguimControlCreateView, self).get_initial()
        # initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(aus_patologia)+1),width=4)
        initial["request"] = self.request
        return initial

    def form_invalid(self, form):
        return super(SeguimControlCreateView, self).form_invalid(form)


@login_required
def ausentismo_eliminar(request, id):
    if not tiene_permiso(request, "aus_abm"):
        return redirect(reverse("principal"))
    aus = ausentismo.objects.get(pk=id, empleado__empresa__pk__in=empresas_habilitadas(request)).delete()
    messages.success(request, "¡Los datos se eliminaron con éxito!")
    return HttpResponseRedirect(reverse("ausentismo_listado"))


@login_required
def ausentismo_eliminar_masivo(request):
    if not tiene_permiso(request, "aus_abm"):
        return redirect(reverse("principal"))
    listado = request.GET.getlist("id")
    ausentismos = ausentismo.objects.filter(
        id__in=listado, empleado__empresa__pk__in=empresas_habilitadas(request)
    ).delete()
    messages.success(request, "¡Los datos se eliminaron con éxito!")
    return HttpResponse(json.dumps(len(listado)), content_type="application/json")


############ PATOLOGIAS ############################


class PatologiaView(VariablesMixin, ListView):
    model = aus_patologia
    template_name = "ausentismos/patologia_listado.html"
    context_object_name = "patologias"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "pat_pantalla"):
            return redirect(reverse("principal"))
        return super(PatologiaView, self).dispatch(*args, **kwargs)


class PatologiaCreateView(VariablesMixin, AjaxCreateView):
    form_class = PatologiaForm
    template_name = "modal/entidades/form_patologia.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "pat_pantalla"):
            return redirect(reverse("principal"))
        return super(PatologiaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(PatologiaCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PatologiaCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(PatologiaCreateView, self).get_initial()
        # initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(aus_patologia)+1),width=4)
        initial["request"] = self.request
        return initial

    def form_invalid(self, form):
        return super(PatologiaCreateView, self).form_invalid(form)


class PatologiaEditView(VariablesMixin, AjaxUpdateView):
    form_class = PatologiaForm
    model = aus_patologia
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_patologia.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "pat_pantalla"):
            return redirect(reverse("principal"))
        return super(PatologiaEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(PatologiaEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PatologiaEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(PatologiaEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(PatologiaEditView, self).get_initial()
        return initial


@login_required
def patologia_baja_alta(request, id):
    patologia = aus_patologia.objects.get(pk=id)
    patologia.baja = not patologia.baja
    patologia.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("patologia_listado"))


############ DIAGNOSTICOS ############################


class DiagnosticoView(VariablesMixin, ListView):
    model = aus_diagnostico
    template_name = "ausentismos/diagnostico_listado.html"
    context_object_name = "diagnosticos"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "diag_pantalla"):
            return redirect(reverse("principal"))
        return super(DiagnosticoView, self).dispatch(*args, **kwargs)


class DiagnosticoCreateView(VariablesMixin, AjaxCreateView):
    form_class = DiagnosticoForm
    template_name = "modal/entidades/form_diagnostico.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "diag_pantalla"):
            return redirect(reverse("principal"))
        return super(DiagnosticoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(DiagnosticoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(DiagnosticoCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(DiagnosticoCreateView, self).get_initial()
        # initial['codigo'] = 'ART'+'{0:0{width}}'.format((ultimoNroId(aus_patologia)+1),width=4)
        initial["request"] = self.request
        return initial

    def form_invalid(self, form):
        return super(DiagnosticoCreateView, self).form_invalid(form)


class DiagnosticoEditView(VariablesMixin, AjaxUpdateView):
    form_class = DiagnosticoForm
    model = aus_diagnostico
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_diagnostico.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "diag_pantalla"):
            return redirect(reverse("principal"))
        return super(DiagnosticoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(DiagnosticoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(DiagnosticoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(DiagnosticoEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(DiagnosticoEditView, self).get_initial()
        return initial


@login_required
def diagnostico_baja_alta(request, id):
    diagnostico = aus_diagnostico.objects.get(pk=id)
    diagnostico.baja = not diagnostico.baja
    diagnostico.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("diagnostico_listado"))


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, "utf-8") for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode("utf-8")


@login_required
def ausencias_importar(request):
    context = {}
    context = getVariablesMixin(request)
    if request.method == "POST":
        form = ImportarAusentismosForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            csv_file = form.cleaned_data["archivo"]
            empresa = form.cleaned_data["empresa"]

            if not csv_file.name.endswith(".csv"):
                messages.error(request, "¡El archivo debe tener extensión .CSV!")
                return HttpResponseRedirect(reverse("importar_empleados"))

            if csv_file.multiple_chunks():
                messages.error(request, "El archivo es demasiado grande (%.2f MB)." % (csv_file.size / (1000 * 1000),))
                return HttpResponseRedirect(reverse("importar_empleados"))

            decoded_file = csv_file.read().decode("latin1").replace(",", "").replace("'", "")
            # decoded_file=decoded_file.decode("latin1")
            io_string = io.StringIO(decoded_file)
            reader = unicode_csv_reader(io_string)

            # DNI;TIPO_AUSENCIA;aus_control;aus_fcontrol;aus_certificado;aus_fcertif;aus_fentrega_certif;aus_fcrondesde;aus_fcronhasta;aus_diascaidos;
            # aus_diasjustif;aus_freintegro;aus_falta;TIPO_ALTA;aus_medico;aus_grupop;aus_diagn;TIPO_ACCIDENTE;art_ndenuncia;art_faccidente;
            # art_fdenuncia;observaciones;descr_altaparc;detalle_acc_art;estudios_partic;estudios_art;recalificac_art
            cant = 0
            try:
                next(reader)  # Omito el Encabezado

                for index, line in enumerate(reader):

                    campos = line[0].split(";")

                    dni = campos[0].strip()

                    if dni == "":
                        continue  # Salta al siguiente

                    try:
                        empl = ent_empleado.objects.get(nro_doc=dni)
                    except:
                        messages.error(request, "Empleado no existente! (%s)" % dni)
                        continue

                    tipoa = campos[1].strip()
                    if tipoa == "":
                        tipoa = None
                    else:
                        ta = dict(TIPO_AUSENCIA)
                        tipoa = [k for k, v in ta.items() if v.upper() == tipoa.upper()][0]

                    if campos[2].strip().upper() == "SI":
                        aus_control = "S"
                    else:
                        aus_control = "N"

                    if campos[3].strip() == "":
                        aus_fcontrol = None
                    else:
                        aus_fcontrol = datetime.datetime.strptime(campos[3], "%d/%m/%Y").date()

                    if campos[4].strip().upper() == "SI":
                        aus_certificado = "S"
                    else:
                        aus_certificado = "N"

                    if campos[5] == "":
                        aus_fcertif = None
                    else:
                        aus_fcertif = datetime.datetime.strptime(campos[5], "%d/%m/%Y").date()
                    if campos[6] == "":
                        aus_fentrega_certif = None
                    else:
                        aus_fentrega_certif = datetime.datetime.strptime(campos[6], "%d/%m/%Y").date()

                    if campos[7] == "":
                        aus_fcrondesde = None
                    else:
                        aus_fcrondesde = datetime.datetime.strptime(campos[7], "%d/%m/%Y").date()
                    if campos[8] == "":
                        aus_fcronhasta = None
                    else:
                        aus_fcronhasta = datetime.datetime.strptime(campos[8], "%d/%m/%Y").date()

                    if campos[9] == "":
                        aus_diascaidos = None
                    else:
                        aus_diascaidos = campos[9].strip()

                    if campos[10] == "":
                        aus_diasjustif = None
                    else:
                        aus_diasjustif = campos[10].strip()

                    if campos[11] == "":
                        aus_freintegro = None
                    else:
                        aus_freintegro = datetime.datetime.strptime(campos[11], "%d/%m/%Y").date()

                    if campos[12] == "":
                        aus_falta = None
                    else:
                        aus_falta = datetime.datetime.strptime(campos[12], "%d/%m/%Y").date()

                    austa = campos[13].strip()
                    if austa == "":
                        aus_tipo_alta = None
                    else:
                        aus_tipo_alta = dict(TIPO_ALTA)
                        aus_tipo_alta = [k for k, v in aus_tipo_alta.items() if v.upper() == austa.upper()][0]

                    aus_medico = campos[14].strip().upper()

                    if aus_medico == "":
                        aus_medico = None
                    else:
                        aus_medico = ent_medico_prof.objects.get_or_create(apellido_y_nombre=aus_medico)[0]

                    aus_grupop = campos[15].strip().upper()
                    if aus_grupop == "":
                        aus_grupop = None
                    else:
                        aus_grupop = aus_patologia.objects.get_or_create(patologia=aus_grupop)[0]

                    aus_diagn = campos[16].strip().upper()
                    if aus_diagn == "":
                        aus_diagn = None
                    else:
                        aus_diagn = aus_diagnostico.objects.get_or_create(diagnostico=aus_diagn)[0]

                    tacc = campos[17].strip()
                    if tacc == "":
                        art_tipo_accidente = None
                    else:
                        art_tipo_accidente = dict(TIPO_ACCIDENTE)
                        art_tipo_accidente = [k for k, v in art_tipo_accidente.items() if v.upper() == tacc.upper()][0]

                    if campos[18] == "":
                        art_ndenuncia = None
                    else:
                        art_ndenuncia = campos[20].strip()

                    if campos[19] == "":
                        art_faccidente = None
                    else:
                        art_faccidente = datetime.datetime.strptime(campos[19], "%d/%m/%Y").date()

                    if campos[20] == "":
                        art_fdenuncia = None
                    else:
                        art_fdenuncia = datetime.datetime.strptime(campos[20], "%d/%m/%Y").date()

                    observaciones = campos[21].strip()
                    descr_altaparc = campos[22].strip()
                    detalle_acc_art = campos[23].strip()
                    estudios_partic = campos[24].strip()
                    estudios_art = campos[25].strip()
                    recalificac_art = campos[26].strip()

                    try:
                        obj, created = ausentismo.objects.update_or_create(
                            empleado=empl,
                            tipo_ausentismo=tipoa,
                            aus_fcrondesde=aus_fcrondesde,
                            aus_fcronhasta=aus_fcronhasta,
                            defaults={
                                "aus_control": aus_control,
                                "aus_fcontrol": aus_fcontrol,
                                "aus_certificado": aus_certificado,
                                "aus_fcertif": aus_fcertif,
                                "aus_fentrega_certif": aus_fentrega_certif,
                                "aus_diascaidos": aus_diascaidos,
                                "aus_diasjustif": aus_diasjustif,
                                "aus_freintegro": aus_freintegro,
                                "aus_falta": aus_falta,
                                "aus_tipo_alta": aus_tipo_alta,
                                "aus_medico": aus_medico,
                                "aus_grupop": aus_grupop,
                                "aus_diagn": aus_diagn,
                                "art_tipo_accidente": art_tipo_accidente,
                                "art_ndenuncia": art_ndenuncia,
                                "art_faccidente": art_faccidente,
                                "art_fdenuncia": art_fdenuncia,
                                "observaciones": observaciones,
                                "descr_altaparc": descr_altaparc,
                                "detalle_acc_art": detalle_acc_art,
                                "estudios_partic": estudios_partic,
                                "estudios_art": estudios_art,
                                "recalificac_art": recalificac_art,
                            },
                        )
                        if created:
                            cant += 1
                    except Exception as e:
                        error = "Línea:%s -> %s " % (index, e)
                        messages.error(request, error)

                messages.success(request, "Se importó el archivo con éxito!<br>(%s ausentismos creados)" % cant)
            except Exception as e:
                print e
                messages.error(request, "Línea:%s -> %s" % (index, e))
    else:
        form = ImportarAusentismosForm(None, None, request=request)
    context["form"] = form
    return render(request, "ausentismos/importar_ausentismos.html", context)


# ************* EMAIL **************


@login_required
def mandarEmail(request, ausencias, fecha, asunto, destinatario, observaciones):
    try:
        mail_destino = []
        mail_destino.append(destinatario)

        try:
            config = configuracion.objects.all().first()
        except configuracion.DoesNotExist:
            raise ValueError

        datos = config.get_datos_mail()
        mensaje_inicial = datos["mensaje_inicial"]
        mail_cuerpo = datos["mail_cuerpo"]
        mail_servidor = datos["mail_servidor"]
        mail_puerto = int(datos["mail_puerto"])
        mail_usuario = datos["mail_usuario"]
        mail_password = str(datos["mail_password"])
        mail_origen = datos["mail_origen"]
        observaciones_finales = observaciones
        context = Context()

        template = "ausentismos/informe_ausentismos.html"
        post_pdf = render_to_pdf(template, locals())

        fecha = fecha
        nombre = "Informe_%s" % fecha

        html_content = get_template("general/email.html").render(
            {"mensaje_inicial": mensaje_inicial, "mail_cuerpo": mail_cuerpo}
        )

        backend = EmailBackend(
            host=mail_servidor, port=mail_puerto, username=mail_usuario, password=mail_password, fail_silently=False
        )
        email = EmailMessage(
            subject="%s" % (asunto), body=html_content, from_email=mail_origen, to=mail_destino, connection=backend
        )
        email.attach("%s.pdf" % nombre, post_pdf, "application/pdf")
        email.content_subtype = "html"
        email.send()
        return True
    except Exception as e:
        print e
        return False


@login_required
def imprimir_ausentismo(request, id):
    template = "ausentismos/ausentismo_impresion.html"
    try:
        ausencia = ausentismo.objects.get(pk=id)
        controles = ausentismo_controles.objects.filter(ausentismo=ausencia).exclude(
            Q(fecha__isnull=True, detalle__isnull=True) | Q(fecha__isnull=True, detalle="")
        )
        controles_pat = ausentismo_controles_patologias.objects.filter(ausentismo=ausencia).exclude(
            Q(fecha__isnull=True, detalle__isnull=True) | Q(fecha__isnull=True, detalle="")
        )
    except Exception as e:
        ausencia = None
        controles_pat = None
        controles = None
        messages.error(request, e)

    context = {}
    context = getVariablesMixin(request)
    try:
        config = configuracion.objects.all().first()
    except Exception as e:
        messages.error(request, e)
    context["a"] = ausencia
    context["controles"] = controles
    context["controles_pat"] = controles_pat
    context["config"] = config
    fecha = hoy()
    context["fecha"] = fecha
    return render_to_pdf_response(request, template, context)


@login_required
def imprimir_historial(request, id):
    template = "ausentismos/historia_clinica_impresion.html"
    empleado = ent_empleado.objects.get(pk=id)
    historial = ausentismo.objects.filter(empleado=empleado, empleado__empresa__pk__in=empresas_habilitadas(request))
    # try:
    #     empleado =  ent_empleado.objects.get(pk=id)
    #     historial =  ausentismo.objects.filter(empleado=empleado,empleado__empresa__pk__in=empresas_habilitadas(request))
    # except Exception as e:
    #        raise Htt

    context = {}
    context = getVariablesMixin(request)
    try:
        config = configuracion.objects.all().first()
    except Exception as e:
        messages.error(request, e)

    context["empleado"] = empleado
    context["historial"] = historial
    context["config"] = config
    fecha = hoy()
    context["fecha"] = fecha
    return render_to_pdf_response(request, template, context)


@login_required
def imprimir_informe(request):
    if request.method == "POST":
        form = ImprimirInformeAusenciasForm(request.POST or None)

        if form.is_valid():
            template = "ausentismos/informe_ausentismos.html"
            fecha = form.cleaned_data["fecha"]
            lista = request.session.get("lista_ausentismos", None)
            observaciones_finales = form.cleaned_data["observaciones"]
            ausencias = (
                ausentismo.objects.filter(id__in=lista, empleado__empresa__pk__in=empresas_habilitadas(request))
                .order_by("fecha_creacion", "aus_fcrondesde", "aus_fcronhasta", "empleado__empresa")
                .select_related("empleado", "empleado__empresa", "aus_diagn", "empleado__trab_cargo")
            )
            cant = len(ausencias)

            context = {}
            context = getVariablesMixin(request)
            try:
                config = configuracion.objects.all().first()
            except configuracion.DoesNotExist:
                raise ValueError
            context["ausencias"] = ausencias
            context["observaciones_finales"] = observaciones_finales
            context["cant"] = cant
            context["config"] = config
            context["fecha"] = fecha
            return render_to_pdf_response(request, template, context)
    else:
        lista = request.GET.getlist("id")
        request.session["lista_ausentismos"] = lista
        form = ImprimirInformeAusenciasForm(initial={"lista": lista})
        variables = locals()
        return render(request, "ausentismos/imprimir_informe_ausentismos_form.html", variables)


def generarInforme(request):
    if request.method == "POST" and request.is_ajax():
        form = InformeAusenciasForm(request.POST or None)
        lista = request.POST.getlist("id")
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            asunto = form.cleaned_data["asunto"]
            destinatario = form.cleaned_data["destinatario"]
            observaciones = form.cleaned_data["observaciones"]

            ausencias = (
                ausentismo.objects.filter(id__in=lista, empleado__empresa__pk__in=empresas_habilitadas(request))
                .order_by("fecha_creacion", "aus_fcrondesde", "aus_fcronhasta", "empleado__empresa")
                .select_related("empleado", "empleado__empresa", "aus_diagn", "empleado__trab_cargo")
            )
            cant = len(ausencias)
            if cant <= 0:
                response = {"cant": 0, "message": "¡Debe seleccionar al menos un Ausentismo!"}
                return HttpResponse(json.dumps(response, default=default), content_type="application/json")
            # blah blah blah
            try:
                if not mandarEmail(request, ausencias, fecha, asunto, destinatario, observaciones):
                    response = {
                        "cant": 0,
                        "message": "El informe no pudo ser enviado! (verifique la dirección de correo del destinatario)",
                    }
                else:
                    response = {"cant": cant, "message": "¡El Informe fué generado/enviado con éxito!."}  # for ok
            except:
                response = {
                    "cant": 0,
                    "message": "El informe no pudo ser enviado! (verifique la dirección de correo del destinatario)",
                }

        else:
            errores = ""
            for err in form.errors:
                errores += "<b>" + err + "</b><br>"
            response = {"cant": 0, "message": "¡Verifique los siguientes datos: <br>" + errores.strip()}

        return HttpResponse(json.dumps(response, default=default), content_type="application/json")
    else:
        form = InformeAusenciasForm(None, initial={"ausentismo_id": ""})
        lista = request.GET.getlist("id")
        ausencias = ausentismo.objects.filter(id__in=lista, empleado__empresa__pk__in=empresas_habilitadas(request))
        variables = locals()
        return render(request, "ausentismos/informe_ausentismos_form.html", variables)


def generarInformeIndividual(request, id):
    if request.method == "POST":
        form = InformeAusenciasForm(request.POST or None)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            asunto = form.cleaned_data["asunto"]
            destinatario = form.cleaned_data["destinatario"]
            observaciones = form.cleaned_data["observaciones"]

            ausencias = ausentismo.objects.filter(id=id)
            cant = len(ausencias)
            if cant <= 0:
                response = {"cant": 0, "message": "¡Debe seleccionar al menos un Ausentismo!"}
                return HttpResponse(json.dumps(response, default=default), content_type="application/json")
            # blah blah blah
            try:
                if not mandarEmail(request, ausencias, fecha, asunto, destinatario, observaciones):
                    response = {
                        "cant": 0,
                        "message": "El informe no pudo ser enviado! (verifique la dirección de correo del destinatario)",
                    }
                else:
                    response = {"cant": cant, "message": "¡El Informe fué generado/enviado con éxito!."}  # for ok
            except:
                response = {
                    "cant": 0,
                    "message": "El informe no pudo ser enviado! (verifique la dirección de correo del destinatario)",
                }

        else:
            errores = ""
            for err in form.errors:
                errores += "<b>" + err + "</b><br>"
            response = {"cant": 0, "message": "¡Verifique los siguientes datos: <br>" + errores.strip()}

        return HttpResponse(json.dumps(response, default=default), content_type="application/json")
    else:
        form = InformeAusenciasForm(None, initial={"ausentismo_id": id})
        ausencias = ausentismo.objects.filter(id=id)
        variables = locals()
        return render(request, "ausentismos/informe_ausentismos_form.html", variables)
