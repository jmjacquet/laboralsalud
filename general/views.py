# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import *
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    DetailView,
)

from ausentismos.models import (
    aus_patologia,
    aus_diagnostico,
    ausentismo,
    ausentismos_del_dia,
)
from entidades.forms import EmpleadoLightForm, EmpresaLightForm
from entidades.models import ent_empleado, ent_empresa, ent_medico_prof
from laboralsalud.utilidades import (
    hoy,
    usuario_actual,
    empresa_actual,
    empresas_habilitadas,
    URL_API,
    mobile,
    esAdmin,
    ultimoMes,
)
from modal.views import AjaxCreateView, AjaxUpdateView
from .forms import (
    TurnosForm,
    ConsultaTurnos,
    ConsultaFechasInicio,
    ConfiguracionForm,
    TurnosLightForm,
)
from .models import turnos, configuracion


class VariablesMixin(object):
    def get_context_data(self, **kwargs):
        from usuarios.views import ver_permisos

        context = super(VariablesMixin, self).get_context_data(**kwargs)
        usr = self.request.user
        try:
            context["usuario"] = usuario_actual(self.request)
        except:
            context["usuario"] = None
        try:
            context["usr"] = usr
        except:
            context["usr"] = None
        try:
            context["empresa"] = empresa_actual(self.request)
        except:
            context["empresa"] = None
        try:
            context["esAdmin"] = self.request.user.userprofile.id_usuario.tipoUsr == 0
        except:
            context["esAdmin"] = False

        permisos_grupo = ver_permisos(self.request)
        context["permisos_grupo"] = permisos_grupo
        context["permisos_empelados"] = (
            ("aus_pantalla" in permisos_grupo)
            or ("empl_pantalla" in permisos_grupo)
            or ("turnos_pantalla" in permisos_grupo)
        )
        context["permisos_indicadores"] = ("indic_pantalla" in permisos_grupo) or (
            "indic_anual_pantalla" in permisos_grupo
        )
        context["permisos_configuracion"] = (
            ("art_pantalla" in permisos_grupo)
            or ("emp_pantalla" in permisos_grupo)
            or ("med_pantalla" in permisos_grupo)
            or ("pat_pantalla" in permisos_grupo)
            or ("diag_pantalla" in permisos_grupo)
            or ("ptrab_pantalla" in permisos_grupo)
            or ("esp_pantalla" in permisos_grupo)
        )

        context["inicio_ausentismos"] = ("inicio_ausentismos" in permisos_grupo) or (
            "inicio_controles" in permisos_grupo
        )
        context["inicio_turnos"] = "inicio_turnos" in permisos_grupo
        context["info_sensible"] = (
            "info_sensible" in permisos_grupo
            or self.request.user.userprofile.id_usuario.tipoUsr == 0
        )
        context["empresas"] = ent_empresa.objects.filter(baja=False)
        context["sitio_mobile"] = mobile(self.request)
        context["hoy"] = hoy()
        # context['EMAIL_CONTACTO'] = EMAIL_CONTACTO
        return context


def getVariablesMixin(request):
    from usuarios.views import ver_permisos

    context = dict({})
    usr = request.user
    try:
        context["usuario"] = usuario_actual(request)
    except:
        context["usuario"] = None

    try:
        context["usr"] = usr
    except:
        context["usr"] = None

    try:
        context["empresa"] = empresa_actual(request)
    except:
        context["empresa"] = None

    try:
        context["esAdmin"] = request.user.userprofile.id_usuario.tipoUsr == 0
    except:
        context["esAdmin"] = False

    permisos_grupo = ver_permisos(request)
    context["permisos_grupo"] = permisos_grupo
    context["permisos_empelados"] = (
        ("aus_pantalla" in permisos_grupo)
        or ("empl_pantalla" in permisos_grupo)
        or ("turnos_pantalla" in permisos_grupo)
    )
    context["permisos_indicadores"] = ("indic_pantalla" in permisos_grupo) or (
        "indic_anual_pantalla" in permisos_grupo
    )
    context["permisos_configuracion"] = (
        ("art_pantalla" in permisos_grupo)
        or ("emp_pantalla" in permisos_grupo)
        or ("med_pantalla" in permisos_grupo)
        or ("med_pantalla" in permisos_grupo)
        or ("pat_pantalla" in permisos_grupo)
        or ("diag_pantalla" in permisos_grupo)
        or ("ptrab_pantalla" in permisos_grupo)
        or ("esp_pantalla" in permisos_grupo)
    )
    context["inicio_ausentismos"] = ("inicio_ausentismos" in permisos_grupo) or (
        "inicio_controles" in permisos_grupo
    )
    context["inicio_turnos"] = "inicio_turnos" in permisos_grupo
    context["info_sensible"] = (
        "info_sensible" in permisos_grupo
        or request.user.userprofile.id_usuario.tipoUsr == 0
    )
    context["empresas"] = ent_empresa.objects.filter(baja=False)
    context["sitio_mobile"] = mobile(request)
    context["hoy"] = hoy()
    return context


class PrincipalView(VariablesMixin, TemplateView):
    template_name = "index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PrincipalView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrincipalView, self).get_context_data(**kwargs)
        busq = None
        if self.request.POST:
            busq = self.request.POST
        elif "principal" in self.request.session:
            busq = self.request.session["principal"]

        form = ConsultaFechasInicio(busq or None)
        fecha1 = hoy()
        fecha2 = hoy()
        if form.is_valid():
            fecha1 = form.cleaned_data["fecha1"] or hoy()
            fecha2 = form.cleaned_data["fecha2"] or hoy()
            self.request.session["principal"] = self.request.POST or busq
        empresas = empresas_habilitadas(self.request)
        ausentismos = (
            ausentismos_del_dia(self.request, fecha1)
            .order_by("-aus_fcontrol")
            .select_related("empleado", "empresa", "aus_grupop", "aus_diagn")
        )
        fechas_control = (
            ausentismo.objects.filter(
                baja=False, aus_fcontrol=fecha1, empresa__pk__in=empresas
            )
            .order_by("-aus_fcontrol")
            .select_related("empleado", "empresa", "aus_grupop", "aus_diagn")
        )
        prox_turnos = turnos.objects.filter(
            turno_empresa__pk__in=empresas, fecha__gte=fecha2
        ).select_related("turno_empleado", "turno_empresa", "usuario_carga")
        context["form"] = form
        context["ausentismo"] = ausentismos
        context["turnos"] = prox_turnos
        context["fechas_control"] = fechas_control
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


def buscarDatosAPICUIT(request):
    try:
        cuit = request.GET["cuit"]
        data = urllib.urlopen(URL_API + cuit).read()
        d = json.loads(data)

        imp = [x["idImpuesto"] for x in d["impuesto"]]
        if 10 in imp:
            id_cat = 1
        elif 11 in imp:
            id_cat = 1
        elif 30 in imp:
            id_cat = 1
        elif 20 in imp:
            id_cat = 6
        elif 32 in imp:
            id_cat = 4
        elif 33 in imp:
            id_cat = 2
        else:
            id_cat = 5
        d.update({"categoria": id_cat})
    except:
        d = []
    return HttpResponse(json.dumps(d), content_type="application/json")


def buscarDatosEntidad(request):
    lista = {}
    id = request.GET["id"]
    e = ent_empleado.objects.filter(pk=id).select_related("art", "empresa", "trab_cargo").first()
    lista = {
        "id": e.id,
        "nro_doc": e.nro_doc,
        "legajo": e.legajo,
        "apellido_y_nombre": e.apellido_y_nombre,
        "fecha_nac": e.fecha_nac,
        "domicilio": e.domicilio,
        "provincia": e.get_provincia_display(),
        "localidad": e.localidad,
        "cod_postal": e.cod_postal,
        "email": e.email,
        "telefono": e.telefono,
        "celular": e.celular,
        "art": e.get_art(),
        "empresa": e.get_empresa(),
        "empr_fingreso": e.empr_fingreso,
        "trab_cargo": e.get_cargo(),
        "trab_fingreso": e.trab_fingreso,
        "trab_fbaja": e.trab_fbaja,
        "trab_armas": e.trab_armas,
        "trab_tareas_dif": e.trab_tareas_dif,
        "trab_preocupac": e.trab_preocupac,
        "trab_preocup_fecha": e.trab_preocup_fecha,
        "edad": e.get_edad,
        "antig_empresa": e.get_antiguedad_empr,
        "antig_trabajo": e.get_antiguedad_trab,
        "id_empresa": e.empresa_id,
    }
    # try:
    #    id = request.GET['id']
    #    entidad = ent_empleado.objects.get(id=id)
    #    qs_json = serializers.serialize('json', entidad)

    # except:
    #  lista= {}
    return HttpResponse(
        json.dumps(lista, cls=DjangoJSONEncoder), content_type="application/json"
    )


# @login_required
def recargar_empleados(request):
    context = {}
    empleados = (ent_empleado.objects.filter(
        empresa_id__in=empresas_habilitadas(request), baja=False).select_related("empresa")
                 .order_by("apellido_y_nombre"))
    context["empleados"] = [{"id": e.pk, "nombre": e.get_empleado()} for e in empleados]
    return HttpResponse(json.dumps(context))


def recargar_empleados_empresa(request, id):
    context = {}
    empleados = (ent_empleado.objects.filter(empresa_id=id, baja=False).select_related("empresa")
    .order_by("apellido_y_nombre"))
    context["empleados"] = [{"id": e.pk, "nombre": e.get_empleado()} for e in empleados]
    return HttpResponse(json.dumps(context))


def recargar_empresas_agrupamiento(request, id):
    context = {}
    empresas_hab = empresas_habilitadas(request)
    empresas = ent_empresa.objects.filter(
        id__in=empresas_hab, baja=False
    ).select_related("casa_central")
    if int(id) > 0:
        empresas = empresas.filter(agrupamiento__id=id)
    lista_empresas = [{"id": e.pk, "nombre": e.get_empresa()} for e in empresas]
    return JsonResponse(lista_empresas, safe=False)


def recargar_medicos(request):
    context = {}
    lista = []
    medicos = ent_medico_prof.objects.filter(baja=False)
    for e in medicos:
        lista.append({"id": e.pk, "nombre": e.get_medico()})
    context["medicos"] = lista
    return HttpResponse(json.dumps(context))


def recargar_diagnosticos(request):
    context = {}
    lista = []
    diagnosticos = aus_diagnostico.objects.filter(baja=False)
    for e in diagnosticos:
        lista.append({"id": e.pk, "nombre": e.diagnostico.upper()})
    context["diagnosticos"] = lista
    return HttpResponse(json.dumps(context))


def recargar_patologias(request):
    context = {}
    lista = []
    patologias = aus_patologia.objects.filter(baja=False)
    for e in patologias:
        lista.append({"id": e.pk, "nombre": e.get_patologia()})
    context["patologias"] = lista
    return HttpResponse(json.dumps(context))


############ TURNOS ############################
from usuarios.views import tiene_permiso


class TurnosView(VariablesMixin, ListView):
    model = turnos
    template_name = "general/turnos_listado.html"
    context_object_name = "turnos"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "turnos_pantalla"):
            return redirect(reverse("principal"))
        return super(TurnosView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TurnosView, self).get_context_data(**kwargs)
        busq = None
        if self.request.POST:
            busq = self.request.POST
        elif "turnos" in self.request.session:
            busq = self.request.session["turnos"]
        form = ConsultaTurnos(self.request.POST or None, request=self.request)
        empresas = empresas_habilitadas(self.request)
        listado = turnos.objects.filter(
            turno_empresa__pk__in=empresas, fecha__gte=ultimoMes()
        )
        if form.is_valid():
            fdesde = form.cleaned_data["fdesde"]
            fhasta = form.cleaned_data["fhasta"]
            empresa = form.cleaned_data["qempresa"]
            empleado = form.cleaned_data["qempleado"]
            estado = form.cleaned_data["qestado"]

            listado = turnos.objects.filter(turno_empresa__pk__in=empresas)

            if fdesde:
                listado = listado.filter(fecha__gte=fdesde)
            if fhasta:
                listado = listado.filter(fecha__lte=fhasta)
            if empresa:
                listado = listado.filter(
                    Q(turno_empresa=empresa) | Q(turno_empresa__casa_central=empresa)
                )
            if empleado:
                listado = listado.filter(
                    Q(turno_empleado__apellido_y_nombre__icontains=empleado)
                    | Q(turno_empleado__nro_doc__icontains=empleado)
                )

            if int(estado) < 3:
                listado = listado.filter(estado=estado)

            self.request.session["turnos"] = self.request.POST or busq

        context["form"] = form
        context["turnos"] = listado.select_related(
            "turno_empleado", "turno_empresa", "usuario_carga"
        )

        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class TurnosCreateView(VariablesMixin, AjaxCreateView):
    form_class = TurnosForm
    template_name = "modal/general/form_turnos.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "turnos_pantalla"):
            return redirect(reverse("principal"))
        return super(TurnosCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # form.instance.empresa = empresa_actual(self.request)
        form.instance.usuario_carga = usuario_actual(self.request)
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(TurnosCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TurnosCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["tipo_form"] = "ALTA"
        kwargs["es_admin"] = esAdmin(self.request)
        return kwargs

    def get_initial(self):
        initial = super(TurnosCreateView, self).get_initial()
        initial["request"] = self.request
        initial["tipo_form"] = "ALTA"
        return initial

    def form_invalid(self, form):
        return super(TurnosCreateView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return reverse("turnos_listado")


class TurnosLightCreateView(VariablesMixin, AjaxCreateView):
    form_class = TurnosLightForm
    template_name = "modal/general/form_turnos_light.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "turnos_pantalla"):
            return redirect(reverse("principal"))
        return super(TurnosLightCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        empresa_form = EmpresaLightForm(prefix="empresa_form")
        empleado_form = EmpleadoLightForm(prefix="empleado_form")
        return self.render_to_response(
            self.get_context_data(
                form=form, empresa_form=empresa_form, empleado_form=empleado_form
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        empresa_form = EmpresaLightForm(self.request.POST, prefix="empresa_form")
        empleado_form = EmpleadoLightForm(self.request.POST, prefix="empleado_form")
        if form.is_valid() and empresa_form.is_valid() and empleado_form.is_valid():
            return self.form_valid(form, empresa_form, empleado_form)
        else:
            return self.form_invalid(
                form=form, empresa_form=empresa_form, empleado_form=empleado_form
            )

    def form_valid(self, form, empresa_form, empleado_form):
        try:
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.usuario_carga = usuario_actual(self.request)

                empresa = empresa_form.save(commit=False)
                empresa.usuario_carga = usuario_actual(self.request)
                empresa.save()

                empleado = empleado_form.save(commit=False)
                empleado.usuario_carga = usuario_actual(self.request)
                empleado.empresa = empresa
                empleado.save()

                self.object.turno_empresa = empresa
                self.object.turno_empleado = empleado
                self.object.save()
                messages.success(self.request, "Los datos se guardaron con éxito!")
        except IntegrityError:
            return self.form_invalid(form, empresa_form, empleado_form)
        return super(TurnosLightCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(TurnosLightCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(TurnosLightCreateView, self).get_initial()
        initial["request"] = self.request
        return initial

    def form_invalid(self, form, empresa_form, empleado_form):
        return super(TurnosLightCreateView, self).form_invalid(
            form=form, empresa_form=empresa_form, empleado_form=empleado_form
        )


class TurnosEditView(VariablesMixin, AjaxUpdateView):
    form_class = TurnosForm
    model = turnos
    pk_url_kwarg = "id"
    template_name = "modal/general/form_turnos.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "turnos_pantalla"):
            return redirect(reverse("principal"))
        return super(TurnosEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(TurnosEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(TurnosEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(TurnosEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["tipo_form"] = "EDICION"
        kwargs["turno"] = self.get_object()
        return kwargs

    def get_initial(self):
        initial = super(TurnosEditView, self).get_initial()
        initial["tipo_form"] = "EDICION"
        return initial

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields["turno_empleado"].widget.attrs["disabled"] = "disabled"
        form.fields["turno_empresa"].widget.attrs["disabled"] = "disabled"
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return reverse("turnos_listado")


class TurnosVerView(VariablesMixin, DetailView):
    model = turnos
    pk_url_kwarg = "id"
    context_object_name = "t"
    template_name = "general/turnos_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TurnosVerView, self).dispatch(*args, **kwargs)


@login_required
def turno_eliminar(request, id):
    if not tiene_permiso(request, "turnos_pantalla"):
        return redirect(reverse("principal"))
    ent = turnos.objects.get(pk=id).delete()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    # return HttpResponseRedirect(reverse("turnos_listado"))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def turno_estado(request, id, estado):
    if not tiene_permiso(request, "turnos_pantalla"):
        return redirect(reverse("principal"))
    ent = turnos.objects.get(pk=id)
    ent.estado = estado
    ent.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # return HttpResponseRedirect(reverse("turnos_listado"))


class ConfiguracionEditView(VariablesMixin, UpdateView):
    form_class = ConfiguracionForm
    model = configuracion
    pk_url_kwarg = "id"
    template_name = "general/configuracion_form.html"
    success_url = "/"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not esAdmin(self.request):
            return redirect(reverse("principal"))
        return super(ConfiguracionEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(ConfiguracionEditView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ConfiguracionEditView, self).get_form_kwargs()
        return kwargs

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        initial = super(ConfiguracionEditView, self).get_initial()
        return initial
