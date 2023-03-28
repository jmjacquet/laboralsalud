# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from __builtin__ import unicode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

from entidades.forms import (
    ARTForm,
    CargoForm,
    EspecialidadForm,
    MedProfForm,
    EmpresaForm,
    EmpleadoForm,
    ConsultaEmpleados,
    EmpresaAgrupamientoForm,
    AgruparEmpleadosForm,
)
from entidades.models import *
from general.views import VariablesMixin
from laboralsalud.utilidades import (
    ultimoNroId,
    usuario_actual,
    empresa_actual,
    empresas_habilitadas,
    default,
)
from modal.views import AjaxCreateView, AjaxUpdateView
from usuarios.views import tiene_permiso


############ ART ############################


class ARTView(VariablesMixin, ListView):
    model = ent_art
    template_name = "entidades/art_listado.html"
    context_object_name = "art"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "art_pantalla"):
            return redirect(reverse("principal"))
        return super(ARTView, self).dispatch(*args, **kwargs)


class ARTCreateView(VariablesMixin, AjaxCreateView):
    form_class = ARTForm
    template_name = "modal/entidades/form_art.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "art_pantalla"):
            return redirect(reverse("principal"))
        return super(ARTCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario_carga = usuario_actual(self.request)
        self.object.save()
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(ARTCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ARTCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(ARTCreateView, self).get_initial()
        initial["codigo"] = "ART" + "{0:0{width}}".format(
            (ultimoNroId(ent_art) + 1), width=4
        )
        initial["request"] = self.request
        return initial

    def form_invalid(self, form):
        return super(ARTCreateView, self).form_invalid(form)


class ARTEditView(VariablesMixin, AjaxUpdateView):
    form_class = ARTForm
    model = ent_art
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_art.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "art_pantalla"):
            return redirect(reverse("principal"))
        return super(ARTEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(ARTEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ARTEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(ARTEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(ARTEditView, self).get_initial()
        return initial


class ARTVerView(VariablesMixin, DetailView):
    model = ent_art
    pk_url_kwarg = "id"
    context_object_name = "art"
    template_name = "entidades/art_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ARTVerView, self).dispatch(*args, **kwargs)


@login_required
def art_baja_alta(request, id):
    if not tiene_permiso(request, "art_pantalla"):
        return redirect(reverse("principal"))
    art = ent_art.objects.get(pk=id)
    art.baja = not art.baja
    art.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("art_listado"))


############ CARGO ############################


class CargoView(VariablesMixin, ListView):
    model = ent_cargo
    template_name = "entidades/cargo_listado.html"
    context_object_name = "cargo"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "ptrab_pantalla"):
            return redirect(reverse("principal"))
        return super(CargoView, self).dispatch(*args, **kwargs)


class CargoCreateView(VariablesMixin, AjaxCreateView):
    form_class = CargoForm
    template_name = "modal/entidades/form_cargo.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "ptrab_pantalla"):
            return redirect(reverse("principal"))
        return super(CargoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(CargoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CargoCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(CargoCreateView, self).get_initial()
        initial["codigo"] = "{0:0{width}}".format((ultimoNroId(ent_cargo) + 1), width=4)
        initial["request"] = self.request
        return initial

    def form_invalid(self, form):
        return super(CargoCreateView, self).form_invalid(form)


class CargoEditView(VariablesMixin, AjaxUpdateView):
    form_class = CargoForm
    model = ent_cargo
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_cargo.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "ptrab_pantalla"):
            return redirect(reverse("principal"))
        return super(CargoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(CargoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CargoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(CargoEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(CargoEditView, self).get_initial()
        return initial


class CargoVerView(VariablesMixin, DetailView):
    model = ent_cargo
    pk_url_kwarg = "id"
    context_object_name = "cargo"
    template_name = "entidades/cargo_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CargoVerView, self).dispatch(*args, **kwargs)


@login_required
def cargo_baja_alta(request, id):
    if not tiene_permiso(request, "ptrab_pantalla"):
        return redirect(reverse("principal"))
    ent = ent_cargo.objects.get(pk=id)
    ent.baja = not ent.baja
    ent.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("cargo_listado"))


############ ESPECIALIDAD ############################


class EspecialidadView(VariablesMixin, ListView):
    model = ent_especialidad
    template_name = "entidades/especialidad_listado.html"
    context_object_name = "esp"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "esp_pantalla"):
            return redirect(reverse("principal"))
        return super(EspecialidadView, self).dispatch(*args, **kwargs)


class EspecialidadCreateView(VariablesMixin, AjaxCreateView):
    form_class = EspecialidadForm
    template_name = "modal/entidades/form_esp.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "esp_pantalla"):
            return redirect(reverse("principal"))
        return super(EspecialidadCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EspecialidadCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EspecialidadCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EspecialidadCreateView, self).get_initial()
        initial["codigo"] = "{0:0{width}}".format(
            (ultimoNroId(ent_especialidad) + 1), width=4
        )
        initial["request"] = self.request
        return initial

    def form_invalid(self, form):
        return super(EspecialidadCreateView, self).form_invalid(form)


class EspecialidadEditView(VariablesMixin, AjaxUpdateView):
    form_class = EspecialidadForm
    model = ent_especialidad
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_esp.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "esp_pantalla"):
            return redirect(reverse("principal"))
        return super(EspecialidadEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EspecialidadEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EspecialidadEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(EspecialidadEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EspecialidadEditView, self).get_initial()
        return initial


class EspecialidadVerView(VariablesMixin, DetailView):
    model = ent_especialidad
    pk_url_kwarg = "id"
    context_object_name = "esp"
    template_name = "entidades/especialidad_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EspecialidadVerView, self).dispatch(*args, **kwargs)


@login_required
def especialidad_baja_alta(request, id):
    if not tiene_permiso(request, "esp_pantalla"):
        return redirect(reverse("principal"))
    ent = ent_especialidad.objects.get(pk=id)
    ent.baja = not ent.baja
    ent.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("especialidad_listado"))


############ MEDICO / PROFESIONAL ############################


class MedProfView(VariablesMixin, ListView):
    model = ent_medico_prof
    template_name = "entidades/med_prof_listado.html"
    context_object_name = "med"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "med_pantalla"):
            return redirect(reverse("principal"))
        return super(MedProfView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MedProfView, self).get_context_data(**kwargs)
        med = ent_medico_prof.objects.all().select_related("especialidad")
        context["med"] = med
        return context


class MedProfCreateView(VariablesMixin, AjaxCreateView):
    form_class = MedProfForm
    template_name = "modal/entidades/form_med_prof.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "med_pantalla"):
            return redirect(reverse("principal"))
        return super(MedProfCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # form.instance.empresa = empresa_actual(self.request)
        # form.instance.usuario = usuario_actual(self.request)
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(MedProfCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MedProfCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(MedProfCreateView, self).get_initial()
        initial["codigo"] = "{0:0{width}}".format(
            (ultimoNroId(ent_medico_prof) + 1), width=4
        )
        initial["request"] = self.request
        initial["tipo_form"] = "ALTA"
        return initial

    def form_invalid(self, form):
        return super(MedProfCreateView, self).form_invalid(form)


class MedProfEditView(VariablesMixin, AjaxUpdateView):
    form_class = MedProfForm
    model = ent_medico_prof
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_med_prof.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "med_pantalla"):
            return redirect(reverse("principal"))
        return super(MedProfEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(MedProfEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MedProfEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(MedProfEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(MedProfEditView, self).get_initial()
        initial["tipo_form"] = "EDICION"
        return initial


class MedProfVerView(VariablesMixin, DetailView):
    model = ent_medico_prof
    pk_url_kwarg = "id"
    context_object_name = "mp"
    template_name = "entidades/medico_prof_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MedProfVerView, self).dispatch(*args, **kwargs)


@login_required
def medico_prof_baja_alta(request, id):
    if not tiene_permiso(request, "med_pantalla"):
        return redirect(reverse("principal"))
    ent = ent_medico_prof.objects.get(pk=id)
    ent.baja = not ent.baja
    ent.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("medico_prof_listado"))


############ EMPRESAS ############################


class EmpresaView(VariablesMixin, ListView):
    model = ent_empresa
    template_name = "entidades/empresa_listado.html"
    context_object_name = "empresas"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "emp_pantalla"):
            return redirect(reverse("principal"))
        return super(EmpresaView, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmpresaView, self).get_context_data(**kwargs)
        empr = ent_empresa.objects.filter(
            id__in=empresas_habilitadas(self.request)
        ).select_related("art", "casa_central", "agrupamiento")
        context["empresas"] = empr
        return context


class EmpresaCreateView(VariablesMixin, AjaxCreateView):
    form_class = EmpresaForm
    template_name = "modal/entidades/form_empresa.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "emp_pantalla"):
            return redirect(reverse("principal"))
        return super(EmpresaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario_carga = usuario_actual(self.request)
        self.object.save()
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EmpresaCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpresaCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EmpresaCreateView, self).get_initial()
        initial["codigo"] = "{0:0{width}}".format(
            (ultimoNroId(ent_empresa) + 1), width=4
        )
        initial["request"] = self.request
        initial["tipo_form"] = "ALTA"
        return initial

    def form_invalid(self, form):
        return super(EmpresaCreateView, self).form_invalid(form)


class EmpresaEditView(VariablesMixin, AjaxUpdateView):
    form_class = EmpresaForm
    model = ent_empresa
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_empresa.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "emp_pantalla"):
            return redirect(reverse("principal"))
        return super(EmpresaEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EmpresaEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EmpresaEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpresaEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EmpresaEditView, self).get_initial()
        initial["tipo_form"] = "EDICION"
        return initial


class EmpresaVerView(VariablesMixin, DetailView):
    model = ent_empresa
    pk_url_kwarg = "id"
    context_object_name = "e"
    template_name = "entidades/empresa_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmpresaVerView, self).dispatch(*args, **kwargs)


@login_required
def empresa_baja_alta(request, id):
    if not tiene_permiso(request, "emp_pantalla"):
        return redirect(reverse("principal"))
    ent = ent_empresa.objects.get(pk=id)
    ent.baja = not ent.baja
    ent.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("empresa_listado"))


############ EMPLEADOS ############################


class EmpleadoView(VariablesMixin, ListView):
    model = ent_empleado
    template_name = "entidades/empleado_listado.html"
    context_object_name = "empleados"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "empl_pantalla"):
            return redirect(reverse("principal"))
        return super(EmpleadoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmpleadoView, self).get_context_data(**kwargs)
        busq = None
        if self.request.POST:
            busq = self.request.POST
        elif "empleados" in self.request.session:
            busq = self.request.session["empleados"]
        form = ConsultaEmpleados(busq or None, request=self.request)
        empresas = empresas_habilitadas(self.request)
        empleados = ent_empleado.objects.filter(
            baja=False, empresa__pk__in=empresas
        ).select_related("empresa", "trab_cargo", "art", "usuario_carga")[:100]
        if form.is_valid():
            qempresa = form.cleaned_data["qempresa"]
            estado = form.cleaned_data["estado"]
            art = form.cleaned_data["art"]
            empleados = ent_empleado.objects.filter(
                empresa__pk__in=empresas
            ).select_related("empresa", "trab_cargo", "art", "usuario_carga")

            if int(estado) == 0:
                empleados = empleados.filter(baja=False)
            elif int(estado) == 1:
                empleados = empleados.filter(baja=True)

            if qempresa:
                empleados = empleados.filter(
                    Q(empresa=qempresa) | Q(empresa__casa_central=qempresa)
                )
            if art:
                empleados = empleados.filter(art=art)

            self.request.session["empleados"] = self.request.POST or busq

        context["form"] = form

        context["empleados"] = empleados

        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class EmpleadoCreateView(VariablesMixin, AjaxCreateView):
    form_class = EmpleadoForm
    template_name = "modal/entidades/form_empleado.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "empl_pantalla"):
            return redirect(reverse("principal"))
        return super(EmpleadoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario_carga = usuario_actual(self.request)
        self.object.save()
        recalcular_cantidad_empleados(self.object.empresa)
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EmpleadoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpleadoCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EmpleadoCreateView, self).get_initial()
        initial[
            "legajo"
        ] = ""  #'{0:0{width}}'.format((ultimoNroId(ent_empleado)+1),width=4)
        initial["request"] = self.request
        empresa = empresa_actual(self.request)
        initial["empresa"] = empresa_actual(self.request)
        if empresa:
            initial["art"] = empresa_actual(self.request).art
        initial["tipo_form"] = "ALTA"
        return initial

    def form_invalid(self, form):
        return super(EmpleadoCreateView, self).form_invalid(form)


class EmpleadoEditView(VariablesMixin, AjaxUpdateView):
    form_class = EmpleadoForm
    model = ent_empleado
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_empleado.html"

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "empl_pantalla"):
            return redirect(reverse("principal"))
        return super(EmpleadoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario_carga = usuario_actual(self.request)
        self.object.save()
        recalcular_cantidad_empleados(self.object.empresa)
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EmpleadoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EmpleadoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(EmpleadoEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EmpleadoEditView, self).get_initial()
        initial["tipo_form"] = "EDICION"
        return initial


class EmpleadoVerView(VariablesMixin, DetailView):
    model = ent_empleado
    pk_url_kwarg = "id"
    context_object_name = "empleados"
    template_name = "entidades/empleado_detalle.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EmpleadoVerView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmpleadoVerView, self).get_context_data(**kwargs)
        empleados = self.object
        context["empleados"] = empleados
        context["adic"] = (
            empleados.trab_factores_riesgo
            or empleados.trab_tareas_dif_det
            or empleados.trab_anteriores
            or empleados.trab_antecedentes
            or empleados.trab_accidentes
            or empleados.trab_vacunas
        )
        return context


@login_required
def empleado_baja_alta(request, id):
    if not tiene_permiso(request, "empl_pantalla"):
        return redirect(reverse("principal"))
    try:
        ent = ent_empleado.objects.get(pk=id)
        ent.baja = not ent.baja
        if ent.baja:
            ent.trab_fbaja = hoy()
        else:
            ent.trab_fbaja = None
        ent.save()
        recalcular_cantidad_empleados(ent.empresa)
        messages.success(request, "¡Los datos se guardaron con éxito!")
    except:
        pass
    return HttpResponseRedirect(reverse("empleado_listado"))


@login_required
def empleado_eliminar_masivo(request):
    if not tiene_permiso(request, "empl_pantalla"):
        return redirect(reverse("principal"))
    listado = request.GET.getlist("id")
    try:
        empleados = ent_empleado.objects.filter(id__in=listado)
        empresa = empleados.first().empresa
        empleados.delete()
        messages.success(request, "¡Los datos se eliminaron con éxito!")
        recalcular_cantidad_empleados(empresa)
    except:
        messages.error(
            request,
            "¡El Empleado no debe tener cargado Ausentismos a su nombre!<br>(elimínelos y vuelva a intentar)",
        )

    return HttpResponse(json.dumps(len(listado)), content_type="application/json")


import csv, io
from .forms import ImportarEmpleadosForm
from general.views import getVariablesMixin


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
def importar_empleados(request):
    if not tiene_permiso(request, "empl_pantalla"):
        return redirect(reverse("principal"))
    ctx = {}
    ctx = getVariablesMixin(request)

    if request.method == "POST":
        form = ImportarEmpleadosForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            csv_file = form.cleaned_data["archivo"]
            empresa = form.cleaned_data["empresa"]
            sobreescribir = form.cleaned_data["sobreescribir"] == "S"

            if not csv_file.name.endswith(".csv"):
                messages.error(request, "¡El archivo debe tener extensión .CSV!")
                return HttpResponseRedirect(reverse("importar_empleados"))

            if csv_file.multiple_chunks():
                messages.error(
                    request,
                    "El archivo es demasiado grande (%.2f MB)."
                    % (csv_file.size / (1000 * 1000),),
                )
                return HttpResponseRedirect(reverse("importar_empleados"))

            decoded_file = (
                csv_file.read().decode("latin1").replace(",", "").replace("'", "")
            )
            io_string = io.StringIO(decoded_file)
            reader = unicode_csv_reader(io_string)
            # DNI;LEGAJO/NRO;APELLIDO;NOMBRE;FECHA_NAC;DOMICILIO;CELULAR;TELEFONO;EMAIL;CP;LOCALIDAD;FECHA_INGR;ART;PUESTO
            cant = 0

            try:
                index = 0
                line = ""
                next(reader)  # Omito el Encabezado
                for index, line in enumerate(reader):
                    campos = line[0].split(";")
                    cant_campos = len(campos)
                    if cant_campos != 14:
                        raise Exception(
                            'La cantidad de campos para el registro es incorrecta!(verifique que no existan ";" ni ")'
                        )

                    dni = campos[0].strip()
                    # dni = str(random.randrange(29000000,40000000))

                    if dni == "":
                        continue  # Salta al siguiente

                    empl = ent_empleado.objects.filter(
                        nro_doc=dni, empresa=empresa
                    ).exists()
                    if empl and not sobreescribir:
                        continue

                    legajo = campos[1].strip()  # nro_legajo
                    apellido = campos[2].strip()  # apellido
                    if apellido == "":
                        raise Exception("El apellido no puede estar vacío!")
                    nombre = campos[3].strip()  # nombre
                    if nombre == "":
                        raise Exception("El nombre no puede estar vacío!")
                    nombre = apellido + " " + nombre
                    fecha = campos[4].strip()
                    try:
                        if fecha == "":
                            fecha_nac = None
                        else:
                            fecha_nac = datetime.datetime.strptime(
                                fecha, "%d/%m/%Y"
                            ).date()  # fecha_nacim
                    except Exception as e:
                        raise Exception("Error en el formato de Fecha!")
                    domicilio = campos[5].strip()  # DOMICILIO
                    celular = campos[6].strip()  # celular
                    telefono = campos[7].strip()  # telefono
                    email = campos[8].strip()  # EMAIL
                    cp = campos[9].strip()  # CP
                    localidad = campos[10].strip()  # LOCALIDAD
                    fecha = campos[11].strip()
                    if fecha == "":
                        fecha_ingr = None
                    else:
                        fecha_ingr = datetime.datetime.strptime(
                            fecha, "%d/%m/%Y"
                        ).date()  # FECHA_INGR

                    art = (
                        campos[12].strip().upper().replace(",", "").replace(".", "")
                    )  # ART
                    if art == "":
                        art = None
                    else:
                        art = ent_art.objects.get_or_create(nombre=art)[0]
                    puesto = (
                        campos[13].strip().upper().replace(",", "").replace(".", "")
                    )  # Puesto
                    if puesto == "":
                        puesto = None
                    else:
                        puesto = ent_cargo.objects.get_or_create(cargo=puesto)[0]
                    try:
                        ent_empleado.objects.update_or_create(
                            nro_doc=dni,
                            empresa=empresa,
                            defaults={
                                "legajo": legajo,
                                "apellido_y_nombre": nombre,
                                "fecha_nac": fecha_nac,
                                "art": art,
                                "trab_cargo": puesto,
                                "domicilio": domicilio,
                                "celular": celular,
                                "telefono": telefono,
                                "email": email,
                                "cod_postal": cp,
                                "localidad": localidad,
                                "empr_fingreso": fecha_ingr,
                            },
                        )
                        cant += 1
                    except Exception as e:
                        error = "Línea:%s -> %s" % (index, e)
                        messages.error(request, error)
                recalcular_cantidad_empleados(empresa)
                messages.success(
                    request,
                    "Se importó el archivo con éxito!<br>(%s empleados creados/actualizados)"
                    % cant,
                )
            except Exception as e:
                messages.error(request, "Línea:%s -> %s" % (index, e))
    else:
        form = ImportarEmpleadosForm(None, None, request=request)
    ctx.update(form=form)

    return render(request, "entidades/importar_empleados.html", context=ctx)


def recalcular_cantidad_empleados(empresa):
    cant = (
        ent_empleado.objects.filter(empresa=empresa, baja=False)
        .filter(Q(trab_fbaja__isnull=True) | Q(trab_fbaja__lt=hoy()))
        .distinct()
        .count()
    )
    empresa.cant_empleados = cant
    empresa.save()


@login_required
def empleado_agrupar(request):
    if not tiene_permiso(request, "empl_pantalla"):
        return redirect(reverse("principal"))
    if request.method == "POST":
        form = AgruparEmpleadosForm(request.POST or None)
        if form.is_valid():
            empresa = form.cleaned_data["empresa"]
            fecha_ingreso = form.cleaned_data["fecha"]
            listado = request.session.get("listado_empleados", None)
            empleados = ent_empleado.objects.filter(id__in=listado)
            cant_cambios = empleados.update(
                empresa=empresa, empr_fingreso=fecha_ingreso
            )

            messages.success(
                request,
                "¡Los datos se guardaron con éxito!<br> Los {} empleados fueron reasignados a {}".format(
                    cant_cambios, empresa
                ),
            )
        else:
            errores = ""
            for err in form.errors:
                errores += "<b>" + err + "</b><br>"
            response = "¡Verifique los siguientes datos: <br>" + errores.strip()
            messages.error(request, response)
        return HttpResponseRedirect(reverse("empleado_listado"))
    else:
        listado = request.GET.getlist("id")
        request.session["listado_empleados"] = listado
        form = AgruparEmpleadosForm(initial={"lista": listado})
        variables = locals()
        return render(request, "entidades/agrupamiento_empleados_form.html", variables)


############ AGRUPAMIENTO EMPRESAS ############################


class EmprAgrupamientoView(VariablesMixin, ListView):
    model = ent_empresa_agrupamiento
    template_name = "entidades/empr_agrupamiento_listado.html"
    context_object_name = "agrupamientos"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "emp_pantalla"):
            return redirect(reverse("principal"))
        return super(EmprAgrupamientoView, self).dispatch(*args, **kwargs)


class EmprAgrupamientoCreateView(VariablesMixin, AjaxCreateView):
    form_class = EmpresaAgrupamientoForm
    template_name = "modal/entidades/form_empr_agrupamiento.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "emp_pantalla"):
            return redirect(reverse("principal"))
        return super(EmprAgrupamientoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EmprAgrupamientoCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EmprAgrupamientoCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EmprAgrupamientoCreateView, self).get_initial()
        initial["request"] = self.request
        initial["tipo_form"] = "ALTA"
        return initial

    def form_invalid(self, form):
        return super(EmprAgrupamientoCreateView, self).form_invalid(form)


class EmprAgrupamientoEditView(VariablesMixin, AjaxUpdateView):
    form_class = EmpresaAgrupamientoForm
    model = ent_empresa_agrupamiento
    pk_url_kwarg = "id"
    template_name = "modal/entidades/form_empr_agrupamiento.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not tiene_permiso(self.request, "emp_pantalla"):
            return redirect(reverse("principal"))
        return super(EmprAgrupamientoEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Los datos se guardaron con éxito!")
        return super(EmprAgrupamientoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(EmprAgrupamientoEditView, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(EmprAgrupamientoEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(EmprAgrupamientoEditView, self).get_initial()
        initial["tipo_form"] = "EDICION"
        return initial


@login_required
def empr_agrupamiento_baja_alta(request, id):
    if not tiene_permiso(request, "emp_pantalla"):
        return redirect(reverse("principal"))
    ent = ent_empresa_agrupamiento.objects.get(pk=id)
    ent.baja = not ent.baja
    ent.save()
    messages.success(request, "¡Los datos se guardaron con éxito!")
    return HttpResponseRedirect(reverse("empr_agrupamiento_listado"))
