# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.contrib import messages
from dateutil.relativedelta import *
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    render_to_response,
    HttpResponseRedirect,
    HttpResponse,
)
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    FormView,
    DetailView,
)
from django.db.models import (
    DateTimeField,
    ExpressionWrapper,
    F,
    DecimalField,
    IntegerField,
)
import json
from decimal import Decimal
from django.db.models import Q, Sum, Count, FloatField, Func, Avg
from django.db.models.functions import Coalesce
import decimal
from easy_pdf.rendering import render_to_pdf_response, render_to_pdf
import calendar

from entidades.models import ent_empresa
from general.views import (
    VariablesMixin,
    getVariablesMixin,
    recargar_empresas_agrupamiento,
)
from laboralsalud.utilidades import (
    ultimo_anio,
    hoy,
    DecimalEncoder,
    MESES,
    empresas_habilitadas,
)
from .forms import ConsultaPeriodo, ConsultaAnual
from ausentismos.models import ausentismo
from usuarios.views import tiene_permiso
from general.models import configuracion

################################################################


def calcular_tasa_ausentismo(dias_caidos_tot, dias_laborables, empleados_tot):
    if empleados_tot > 0:
        tasa_ausentismo = (
            Decimal(dias_caidos_tot) / Decimal(dias_laborables * empleados_tot)
        ) * 100
        tasa_ausentismo = Decimal(tasa_ausentismo).quantize(
            Decimal("0.01"), decimal.ROUND_HALF_UP
        )
    else:
        return 0
    return tasa_ausentismo


def calcular_empleados_empresas(empresas_list):
    """
    Calcula la cantidad de empleados de un listado de empresas
    (si hay casas centrales y sucursales debe filtrar para que no se repitan los empleados)
    """
    empl = 0
    if not empresas_list:
        return empl
    empresas = ent_empresa.objects.filter(id__in=empresas_list)
    for e in empresas:
        if not e.casa_central:
            empl += e.cantidad_empleados()
        elif e.casa_central.id not in empresas_list:
            empl += e.cantidad_empleados()
    return empl


@login_required
def reporte_resumen_periodo(request):
    if not tiene_permiso(request, "indic_pantalla"):
        return redirect(reverse("principal"))
    template = "reportes/resumen_periodo.html"
    form = ConsultaPeriodo(request.POST or None, request=request)
    fecha = date.today()
    fdesde = ultimo_anio()
    fhasta = hoy()
    context = {}
    context = getVariablesMixin(request)
    empresas_list = []
    empresa = None
    agrupamiento = None
    filtro = ""
    if form.is_valid():
        periodo = form.cleaned_data["periodo"]
        empresa = form.cleaned_data["empresa"]
        agrupamiento = form.cleaned_data["agrupamiento"]
        empleado = form.cleaned_data["empleado"]
        tipo_ausentismo = form.cleaned_data["tipo_ausentismo"]
        trab_cargo = form.cleaned_data["trab_cargo"]
        fdesde = date(periodo.year, periodo.month, 1)
        fhasta = date(
            periodo.year,
            periodo.month,
            calendar.monthrange(periodo.year, periodo.month)[1],
        )
        filtro = "Período: %s " % (periodo.strftime("%m/%Y"))
        ausentismos = ausentismo.ausentismos_activos.filter(
            Q(aus_fcrondesde__gte=fdesde, aus_fcrondesde__lte=fhasta)
            | Q(aus_fcronhasta__gte=fdesde, aus_fcronhasta__lte=fhasta)
            | Q(aus_fcrondesde__lt=fdesde, aus_fcronhasta__gt=fhasta)
        )
        if agrupamiento and not empresa:
            data = recargar_empresas_agrupamiento(request, agrupamiento.id)
            empresas_list = [d["id"] for d in json.loads(data.content)]
            q_empresas = ent_empresa.objects.filter(Q(id__in=empresas_list)|Q(casa_central__id__in=empresas_list))
            empresas_list = list(q_empresas.values_list('id', flat=True))
        elif empresa:
            if empresa.casa_central:
                empresas_list = list([empresa.pk])
            else:
                empresas_list = [
                    e.id
                    for e in ent_empresa.objects.filter(
                        Q(id=empresa.id) | Q(casa_central=empresa)
                    )
                ]
        else:
            empresas_list = [
                d["id"]
                for d in json.loads(recargar_empresas_agrupamiento(request, 0).content)
            ]
        ausentismos = ausentismos.filter(empleado__empresa__id__in=empresas_list)

        if empleado:
            ausentismos = ausentismos.filter(
                Q(empleado__apellido_y_nombre__icontains=empleado)
                | Q(empleado__nro_doc__icontains=empleado)
            )
            filtro = filtro + " - Empleado: %s" % (empleado)
        if trab_cargo:
            ausentismos = ausentismos.filter(empleado__trab_cargo=trab_cargo)
            filtro += " - Puesto de Trabajo: %s" % (trab_cargo)
        if int(tipo_ausentismo) > 0:
            ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))
    else:
        ausentismos = None
    context["form"] = form
    context["fecha"] = fecha
    context["fdesde"] = fdesde
    context["fhasta"] = fhasta
    context["ausentismos"] = ausentismos
    context["empresa"] = empresa
    context["agrupamiento"] = agrupamiento
    # _tipo_reporte =
    context["titulo_reporte"] = "%s  - %s" % (
        ("Empresa: %s" % empresa if empresa else "Sector: %s" % agrupamiento),
        filtro,
    )
    context["filtro"] = filtro
    context["pie_pagina"] = "Sistemas Laboral Salud - %s" % (fecha.strftime("%d/%m/%Y"))
    dias_laborales = 0
    dias_caidos_tot = 0
    empleados_tot = 0
    dias_trab_tot = 0
    tasa_ausentismo = 0
    aus_total = None
    aus_inc = None
    aus_acc = None
    aus_acc2 = None
    aus_x_grupop = None
    max_grupop = 0
    dias_laborables = int((fhasta - fdesde).days + 1)
    empl_mas_faltadores = []
    porc_dias_trab_tot = 100
    if ausentismos:
        empleados_tot = calcular_empleados_empresas(empresas_list)
        dias_caidos_tot = dias_ausentes(fdesde, fhasta, ausentismos)
        dias_trab_tot = (dias_laborables * empleados_tot) - dias_caidos_tot
        tasa_ausentismo = calcular_tasa_ausentismo(
            dias_caidos_tot, dias_laborables, empleados_tot
        )
        porc_dias_trab_tot = 100 - tasa_ausentismo

        ta_cant_empls = ausentismos.values("empleado").distinct().count()
        tp_cant_empls = empleados_tot - ta_cant_empls

        aus_total = {
            "dias_caidos_tot": dias_caidos_tot,
            "empleados_tot": empleados_tot,
            "dias_trab_tot": dias_trab_tot,
            "tasa_ausentismo": tasa_ausentismo,
            "dias_laborables": dias_laborables,
            "porc_dias_trab_tot": porc_dias_trab_tot,
            "ta_cant_empls": ta_cant_empls,
            "tp_cant_empls": tp_cant_empls,
        }

        # AUSENTISMO INCULPABLE
        ausentismos_inc = ausentismos.filter(tipo_ausentismo=1)
        if ausentismos_inc:
            empleados_inc = ausentismos_inc.values("empleado").distinct().count()
            # empleados_tot = 77
            totales = tot_ausentes_inc(fdesde, fhasta, ausentismos_inc)
            dias_caidos_tot = totales[0]
            # dias_caidos_tot = 67
            dias_trab_tot = (dias_laborables * empleados_tot) - dias_caidos_tot
            tasa_ausentismo = calcular_tasa_ausentismo(
                dias_caidos_tot, dias_laborables, empleados_tot
            )
            agudos = totales[1]
            graves = totales[2]
            empl_agudos = totales[3]
            empl_graves = totales[4]
            porc_agudos = (Decimal(agudos) / Decimal(dias_caidos_tot)) * 100
            porc_cronicos = (Decimal(graves) / Decimal(dias_caidos_tot)) * 100
            tot_agudos = int(empl_agudos)
            tot_cronicos = int(empl_graves)
            porc_agudos = Decimal(porc_agudos).quantize(
                Decimal("0.01"), decimal.ROUND_HALF_UP
            )
            porc_cronicos = Decimal(porc_cronicos).quantize(
                Decimal("0.01"), decimal.ROUND_HALF_UP
            )
            porc_dias_trab_tot = 100 - tasa_ausentismo
            inc_cant_empls = empleados_inc
            noinc_cant_empls = empleados_tot - inc_cant_empls
            aus_inc = {
                "dias_caidos_tot": dias_caidos_tot,
                "empleados_tot": empleados_tot,
                "dias_trab_tot": dias_trab_tot,
                "tasa_ausentismo": tasa_ausentismo,
                "dias_laborables": dias_laborables,
                "porc_dias_trab_tot": porc_dias_trab_tot,
                "porc_agudos": porc_agudos,
                "porc_cronicos": porc_cronicos,
                "inc_cant_empls": inc_cant_empls,
                "noinc_cant_empls": noinc_cant_empls,
                "tot_agudos": tot_agudos,
                "tot_cronicos": tot_cronicos,
            }

        # AUSENTISMO ACCIDENTES
        ausentismos_acc = ausentismos.filter(tipo_ausentismo=2)
        if ausentismos_acc:
            dias_caidos_tot = dias_ausentes(fdesde, fhasta, ausentismos_acc)
            dias_trab_tot = (dias_laborables * empleados_tot) - dias_caidos_tot
            tasa_ausentismo = calcular_tasa_ausentismo(
                dias_caidos_tot, dias_laborables, empleados_tot
            )
            if tasa_ausentismo > 0:
                porc_dias_trab_tot = 100 - tasa_ausentismo
                tot_accidentes = ausentismos_acc.count()
                acc_empls = ausentismos_acc.values("empleado").distinct().count()
                noacc_empls = empleados_tot - acc_empls
                acc_denunciados = ausentismos_acc.exclude(
                    Q(art_ndenuncia__isnull=True) | Q(art_ndenuncia__exact="")
                )
                denunciados_empl = acc_denunciados.values("empleado").distinct().count()
                acc_denunciados = (
                    Decimal(acc_denunciados.count()) / Decimal(tot_accidentes)
                ) * 100
                acc_sin_denunciar = ausentismos_acc.filter(
                    Q(art_ndenuncia__isnull=True) | Q(art_ndenuncia__exact="")
                )
                if not acc_sin_denunciar:
                    sin_denunciar_empl = 0
                    acc_sin_denunciar = 0
                else:
                    sin_denunciar_empl = (
                        acc_sin_denunciar.values("empleado").distinct().count()
                    )
                    acc_sin_denunciar = (
                        Decimal(acc_sin_denunciar.count()) / Decimal(tot_accidentes)
                    ) * 100
                aus_acc2 = {
                    "acc_denunciados": acc_denunciados,
                    "acc_sin_denunciar": acc_sin_denunciar,
                    "denunciados_empl": denunciados_empl,
                    "sin_denunciar_empl": sin_denunciar_empl,
                }
                acc_itinere = ausentismos_acc.filter(art_tipo_accidente=2)
                itinere_empl = acc_itinere.values("empleado").distinct().count()
                acc_itinere = (
                    Decimal(acc_itinere.count()) / Decimal(tot_accidentes)
                ) * 100
                acc_trabajo = ausentismos_acc.filter(art_tipo_accidente=1)
                trabajo_empl = acc_trabajo.values("empleado").distinct().count()
                acc_trabajo = (
                    Decimal(acc_trabajo.count()) / Decimal(tot_accidentes)
                ) * 100
                aus_acc = {
                    "dias_caidos_tot": dias_caidos_tot,
                    "empleados_tot": empleados_tot,
                    "dias_trab_tot": dias_trab_tot,
                    "tasa_ausentismo": tasa_ausentismo,
                    "dias_laborables": dias_laborables,
                    "porc_dias_trab_tot": porc_dias_trab_tot,
                    "tot_accidentes": tot_accidentes,
                    "acc_itinere": acc_itinere,
                    "acc_trabajo": acc_trabajo,
                    "acc_empls": acc_empls,
                    "noacc_empls": noacc_empls,
                    "itinere_empl": itinere_empl,
                    "trabajo_empl": trabajo_empl,
                }
            else:
                aus_acc = None

        aus_grupop = (
            ausentismos.values("aus_grupop__patologia", "aus_grupop__id")
            .annotate(total=Count("aus_grupop"))
            .order_by("-total")[:5]
        )
        aus_x_grupop = []
        for a in aus_grupop:
            aus = ausentismos.filter(aus_grupop__id=a.get("aus_grupop__id"))
            dias = dias_ausentes(fdesde, fhasta, aus)
            aus_x_grupop.append({"patologia": a.get("aus_grupop__patologia"),
                             "total": a.get("total"),
                             "dias": dias})
        aus_x_grupop = sorted(
            aus_x_grupop, key=lambda i: (i["total"], i["dias"]), reverse=True
        )

        max_grupop = aus_x_grupop[0]["total"] + 1

        empl_mas_faltadores = []
        for a in ausentismos.select_related("empleado"):
            dias = dias_ausentes_tot(fdesde, fhasta, a)
            empl_mas_faltadores.append({"empleado": a.empleado, "dias": dias})
        empl_mas_faltadores = sorted(
            empl_mas_faltadores, key=lambda i: i["dias"], reverse=True
        )
    context["aus_total"] = aus_total
    context["aus_inc"] = aus_inc
    context["aus_acc"] = aus_acc
    context["aus_acc2"] = aus_acc2
    context["aus_x_grupop"] = aus_x_grupop
    context["max_grupop"] = max_grupop
    context["dias_laborables"] = dias_laborables
    context["empl_mas_faltadores"] = empl_mas_faltadores[:10]
    if ("pdf" in request.POST) and (aus_total):
        aus_tot_image = request.POST.get("aus_tot_image", None)
        aus_inc_image = request.POST.get("aus_inc_image", None)
        aus_inc2_image = request.POST.get("aus_inc2_image", None)
        aus_acc_image = request.POST.get("aus_acc_image", None)
        aus_acc2_image = request.POST.get("aus_acc2_image", None)
        aus_acc3_image = request.POST.get("aus_acc3_image", None)
        aus_grp_image = request.POST.get("aus_grp_image", None)
        template = "reportes/reporte_periodo.html"
        context["aus_tot_image"] = aus_tot_image
        context["aus_inc_image"] = aus_inc_image
        context["aus_inc2_image"] = aus_inc2_image
        context["aus_acc_image"] = aus_acc_image
        context["aus_acc2_image"] = aus_acc2_image
        context["aus_acc3_image"] = aus_acc3_image
        context["aus_grp_image"] = aus_grp_image
        return render_to_pdf_response(request, template, context)
    return render(request, template, context)


@login_required
def reporteResumenAnual(request):
    if not tiene_permiso(request, "indic_pantalla"):
        return redirect(reverse("principal"))
    template_name = "reportes/resumen_anual.html"
    form = ConsultaAnual(request.POST or None, request=request)
    fecha = date.today()
    fdesde = ultimo_anio()
    fhasta = hoy()
    context = {}
    context = getVariablesMixin(request)
    empresas_list = []
    empresa = None
    agrupamiento = None
    filtro = ""
    max_grupop = 20
    if form.is_valid():
        periodo_desde = form.cleaned_data["periodo_desde"]
        periodo_hasta = form.cleaned_data["periodo_hasta"]
        agrupamiento = form.cleaned_data["agrupamiento"]
        empresa = form.cleaned_data["empresa"]
        empleado = form.cleaned_data["empleado"]
        tipo_ausentismo = form.cleaned_data["tipo_ausentismo"]
        trab_cargo = form.cleaned_data["trab_cargo"]

        fdesde = date(periodo_desde.year, periodo_desde.month, 1)
        fhasta = date(
            periodo_hasta.year,
            periodo_hasta.month,
            calendar.monthrange(periodo_hasta.year, periodo_hasta.month)[1],
        )

        ausentismos = ausentismo.ausentismos_activos.filter(
            Q(aus_fcrondesde__gte=fdesde, aus_fcrondesde__lte=fhasta)
            | Q(aus_fcronhasta__gte=fdesde, aus_fcronhasta__lte=fhasta)
            | Q(aus_fcrondesde__lt=fdesde, aus_fcronhasta__gt=fhasta)
        )
        filtro = "Período desde %s al %s" % (
            fdesde.strftime("%m/%Y"),
            fhasta.strftime("%m/%Y"),
        )
        if agrupamiento and not empresa:
            data = recargar_empresas_agrupamiento(request, agrupamiento.id)
            empresas_list = [d["id"] for d in json.loads(data.content)]
            q_empresas = ent_empresa.objects.filter(Q(id__in=empresas_list) | Q(casa_central__id__in=empresas_list))
            empresas_list = list(q_empresas.values_list('id', flat=True))
        elif empresa:
            if empresa.casa_central:
                empresas_list = list([empresa.pk])
            else:
                empresas_list = [
                    e.id
                    for e in ent_empresa.objects.filter(
                        Q(id=empresa.id) | Q(casa_central=empresa)
                    )
                ]
        else:
            empresas_list = [
                d["id"]
                for d in json.loads(recargar_empresas_agrupamiento(request, 0).content)
            ]
        ausentismos = ausentismos.filter(empleado__empresa__id__in=empresas_list)

        if empleado:
            ausentismos = ausentismos.filter(
                Q(empleado__apellido_y_nombre__icontains=empleado)
                | Q(empleado__nro_doc__icontains=empleado)
            )
        if trab_cargo:
            ausentismos = ausentismos.filter(empleado__trab_cargo=trab_cargo)
            filtro += " - Puesto de Trabajo: %s" % (trab_cargo)
        if int(tipo_ausentismo) > 0:
            ausentismos = ausentismos.filter(tipo_ausentismo=int(tipo_ausentismo))
    else:
        ausentismos = None
    context["form"] = form
    context["fecha"] = fecha
    context["fdesde"] = fdesde
    context["fhasta"] = fhasta
    context["ausentismos"] = ausentismos
    context["empresa"] = empresa
    context["agrupamiento"] = agrupamiento

    dias_laborales = 0
    dias_caidos_tot = 0
    empleados_tot = 0
    dias_trab_tot = 0
    tasa_ausentismo = 0
    aus_total = None
    aus_inc = None
    aus_acc = None
    dias_laborables = 0
    porc_dias_trab_tot = 100
    totales = []
    inculpables = []
    accidentes = []
    enfermos = []
    datos_tabla = []
    import time
    from dateutil.rrule import rrule, MONTHLY

    meses = [
        [int(dt.strftime("%m")), int(dt.strftime("%Y"))]
        for dt in rrule(MONTHLY, dtstart=fdesde, until=fhasta)
    ]

    # import locale
    # locale.setlocale(locale.LC_ALL, '')
    listado_meses = [
        "%s%s" % (MESES[int(dt.strftime("%m")) - 1][1].upper(), (dt.strftime("%Y")))
        for dt in rrule(MONTHLY, dtstart=fdesde, until=fhasta)
    ]
    if ausentismos:
        empleados_tot = calcular_empleados_empresas(empresas_list)
        for m in meses:
            dias_laborables = int(dias_mes(m[0], m[1], fdesde, fhasta))

            ausencias = en_mes_anio(m[0], m[1], ausentismos)

            qs_totales = ausencias
            ausenc_totales = dias_ausentes_mes(m[0], m[1], ausencias)

            empl_totales = empleados_tot
            dias_trab_tot = (dias_laborables * empl_totales) - ausenc_totales

            if ausenc_totales > 0:
                tasa_total = calcular_tasa_ausentismo(
                    ausenc_totales, dias_laborables, empl_totales
                )
            else:
                tasa_total = 0
            ta_cant_empls = qs_totales.values("empleado").distinct().count()

            totales.append({"y": tasa_total, "custom": {"empleados": ta_cant_empls}})

            qs_inculpables = ausencias.filter(tipo_ausentismo=1)
            ausenc_inculp = dias_ausentes_mes(m[0], m[1], qs_inculpables)
            # empl_tot_inculp= qs_inculpables.values('empleado').distinct().count()
            empl_tot_inculp = empleados_tot
            dias_trab_tot = (dias_laborables * empl_tot_inculp) - ausenc_inculp
            if ausenc_inculp > 0:
                tasa_inclup = calcular_tasa_ausentismo(
                    ausenc_inculp, dias_laborables, empl_tot_inculp
                )
            else:
                tasa_inclup = 0
            empl_inculp = qs_inculpables.values("empleado").distinct().count()
            inculpables.append({"y": tasa_inclup, "custom": {"empleados": empl_inculp}})

            qs_accidentes = ausencias.filter(tipo_ausentismo=2)
            ausenc_acc = dias_ausentes_mes(m[0], m[1], qs_accidentes)
            # ausenc_acc = qs_accidentes.count()
            # empl_tot_acc= qs_accidentes.values('empleado').distinct().count()
            empl_tot_acc = empleados_tot
            dias_trab_tot = (dias_laborables * empl_tot_acc) - ausenc_acc
            if ausenc_acc > 0:
                tasa_acc = calcular_tasa_ausentismo(
                    ausenc_acc, dias_laborables, empl_tot_acc
                )
            else:
                tasa_acc = 0
            empl_acc = qs_accidentes.values("empleado").distinct().count()
            accidentes.append({"y": tasa_acc, "custom": {"empleados": empl_acc}})

            qs_enfermos = ausencias.filter(tipo_ausentismo=3)
            ausenc_enf = dias_ausentes_mes(m[0], m[1], qs_enfermos)
            # ausenc_enf = qs_enfermos.count()
            # empl_tot_enf= qs_enfermos.values('empleado').distinct().count()
            empl_tot_enf = empleados_tot
            dias_trab_tot = (dias_laborables * empl_tot_enf) - ausenc_enf
            if ausenc_enf > 0:
                tasa_enf = calcular_tasa_ausentismo(
                    ausenc_enf, dias_laborables, empl_tot_enf
                )
            else:
                tasa_enf = 0

            enfermos.append(tasa_enf)

            datos_tabla.append(
                {
                    "mes": m,
                    "tasa_total": tasa_total,
                    "ta_cant_empls": ta_cant_empls,
                    "tasa_inclup": tasa_inclup,
                    "empl_inculp": empl_inculp,
                    "tasa_acc": tasa_acc,
                    "empl_acc": empl_acc,
                }
            )

        aus_x_grupop_tot = (
            ausentismos.values("aus_grupop__pk", "aus_grupop__patologia")
            .annotate(total=Count("aus_grupop"))
            .order_by("-total")[:4]
        )

        id_grupos = [int(x["aus_grupop__pk"]) for x in aus_x_grupop_tot]

        listado = []

        for x in aus_x_grupop_tot:
            nombre = x["aus_grupop__patologia"]
            id = x["aus_grupop__pk"]
            datos = []
            for m in meses:
                ausencias = en_mes_anio(m[0], m[1], ausentismos)
                aus_x_grupop = list(
                    ausencias.filter(aus_grupop__pk__in=id_grupos)
                    .values("aus_grupop__patologia", "aus_grupop__pk")
                    .annotate(total=Count("aus_grupop"))
                    .order_by("-total")
                    .values("aus_grupop__patologia", "aus_grupop__pk", "total")
                )
                total = sum(
                    [int(p["total"]) for p in aus_x_grupop if id == p["aus_grupop__pk"]]
                )
                datos.append(total)
            listado.append(dict(name=nombre, data=datos))

        if aus_x_grupop:
            max_grupop = max([max(l["data"]) for l in listado])

        context["max_grupop"] = max_grupop
        context["inculpables"] = json.dumps(inculpables, cls=DecimalEncoder)
        context["accidentes"] = json.dumps(accidentes, cls=DecimalEncoder)
        context["enfermos"] = json.dumps(enfermos, cls=DecimalEncoder)
        context["totales"] = json.dumps(totales, cls=DecimalEncoder)
        context["grupop"] = listado

    else:
        context["inculpables"] = None
        context["accidentes"] = None
        context["enfermos"] = None
        context["totales"] = None
        context["grupop"] = None

    context["listado_meses"] = json.dumps(listado_meses, cls=DecimalEncoder)
    context["datos_tabla"] = datos_tabla
    context["empresa"] = empresa
    context["titulo_reporte"] = "%s  - %s" % (
        ("Empresa: %s" % empresa if empresa else "Sector: %s" % agrupamiento),
        filtro,
    )
    context["filtro"] = filtro
    context["pie_pagina"] = "Sistemas Laboral Salud - %s" % (fecha.strftime("%d/%m/%Y"))

    if ("pdf" in request.POST) and (ausentismos):
        aus_tot_image = request.POST.get("aus_tot_image", None)
        aus_grupop_image = request.POST.get("aus_grupop_image", None)
        template_name = "reportes/reporte_anual.html"
        context["aus_tot_image"] = aus_tot_image
        context["aus_grupop_image"] = aus_grupop_image

        return render_to_pdf_response(request, template_name, context)
    return render(request, template_name, context)


######################################################################################


def en_mes_anio(mes, anio, ausentismos):
    d_fmt = "{0:>02}/{1:>02}/{2}"
    fdesde = datetime.strptime(d_fmt.format(1, mes, anio), "%d/%m/%Y").date()
    ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
    fhasta = datetime.strptime(
        d_fmt.format(ultimo_dia_mes, mes, anio), "%d/%m/%Y"
    ).date()
    ausencias = ausentismos.filter(
        Q(aus_fcrondesde__range=[fdesde, fhasta])
        | Q(aus_fcronhasta__range=[fdesde, fhasta])
        | Q(aus_fcrondesde__lt=fdesde, aus_fcronhasta__gt=fhasta)
    )
    return ausencias


def dias_mes(mes, anio, fdesde, fhasta):
    d_fmt = "{0:>02}/{1:>02}/{2}"
    fini = datetime.strptime(d_fmt.format(1, mes, anio), "%d/%m/%Y").date()
    ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
    ffin = datetime.strptime(d_fmt.format(ultimo_dia_mes, mes, anio), "%d/%m/%Y").date()
    if fdesde >= fini:
        fini = fdesde
    if fhasta <= ffin:
        ffin = fhasta

    return (ffin - fini).days + 1


def dias_ausentes(fdesde, fhasta, ausentismos):
    tot = 0
    for a in ausentismos:
        tot += dias_ausentes_tot(fdesde, fhasta, a)
    return tot


def dias_ausentes_tot(fdesde, fhasta, a):
    fini = a.aus_fcrondesde
    ffin = a.aus_fcronhasta
    if fdesde >= fini:
        fini = fdesde
    if fhasta <= ffin:
        ffin = fhasta
    tot = (ffin - fini).days + 1
    return tot


def dias_ausentes_mes(mes, anio, ausentismos):
    tot = 0
    d_fmt = "{0:>02}/{1:>02}/{2}"
    fdesde = datetime.strptime(d_fmt.format(1, mes, anio), "%d/%m/%Y").date()
    ultimo_dia_mes = calendar.monthrange(anio, mes)[1]
    fhasta = datetime.strptime(
        d_fmt.format(ultimo_dia_mes, mes, anio), "%d/%m/%Y"
    ).date()

    for a in ausentismos:
        fini = a.aus_fcrondesde
        ffin = a.aus_fcronhasta

        if fdesde >= fini:
            fini = fdesde
        if fhasta <= ffin:
            ffin = fhasta
        dif = (ffin - fini).days + 1

        tot += dif
    return tot


def tot_ausentes_inc(fdesde, fhasta, ausentismos):
    parcial, agudos, graves = 0, 0, 0
    empl_agudos, empl_graves = 0, 0
    tot = 0
    for a in ausentismos:
        fini = a.aus_fcrondesde
        ffin = a.aus_fcronhasta

        if fdesde >= fini:
            fini = fdesde
        if fhasta <= ffin:
            ffin = fhasta
        parcial = (ffin - fini).days + 1
        tot += parcial
        if parcial < 30:
            agudos += parcial
            empl_agudos += 1
        else:
            graves += parcial
            empl_graves += 1
    return [tot, agudos, graves, empl_agudos, empl_graves]
