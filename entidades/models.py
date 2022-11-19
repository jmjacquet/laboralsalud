# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from laboralsalud.utilidades import *

# from usuarios.models import *
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q


class ent_cargo(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    cargo = models.CharField(max_length=200)
    baja = models.BooleanField(default=False)

    class Meta:
        db_table = "ent_cargo"
        ordering = [
            "cargo",
        ]

    def __unicode__(self):
        return "%s" % self.cargo

    def get_cargo(self):
        return unicode(self.cargo)


class ent_especialidad(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    especialidad = models.CharField(max_length=200)
    baja = models.BooleanField(default=False)

    class Meta:
        db_table = "ent_especialidad"
        ordering = [
            "especialidad",
        ]

    def __unicode__(self):
        return "%s" % self.especialidad


class ent_empresa_agrupamiento(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    descripcion = models.CharField(max_length=200)
    baja = models.BooleanField(default=False)

    class Meta:
        db_table = "ent_empresa_agrupamiento"
        ordering = [
            "descripcion",
        ]

    def __unicode__(self):
        return "%s" % self.descripcion


# Tabla de la Base de Configuracion


class ent_medico_prof(models.Model):
    apellido_y_nombre = models.CharField("Apellido y Nombre", max_length=200)
    codigo = models.CharField("Código", max_length=50, blank=True, null=True)
    cuit = models.CharField("CUIT", max_length=50, blank=True, null=True)
    nro_doc = models.CharField("Documento", max_length=50, blank=True, null=True)
    domicilio = models.CharField("Domicilio", max_length=200, blank=True, null=True)
    provincia = models.IntegerField(
        "Provincia", choices=PROVINCIAS, blank=True, null=True, default=12
    )
    localidad = models.CharField("Localidad", max_length=100, blank=True, null=True)
    cod_postal = models.CharField("CP", max_length=50, blank=True, null=True)
    email = models.EmailField("Email", blank=True)
    telefono = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    celular = models.CharField("Celular", max_length=50, blank=True, null=True)
    especialidad = models.ForeignKey(
        ent_especialidad,
        db_column="especialidad",
        blank=True,
        null=True,
        related_name="med_especialidad",
        on_delete=models.SET_NULL,
    )
    observaciones = models.TextField("Observaciones", blank=True, null=True)

    baja = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modif = models.DateTimeField(auto_now=True)
    usuario_carga = models.ForeignKey(
        "usuarios.UsuUsuario",
        db_column="usuario_carga",
        blank=True,
        null=True,
        related_name="med_usuario_carga",
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "ent_medico_prof"
        ordering = ["apellido_y_nombre", "codigo"]

    def __unicode__(self):
        return "%s" % (self.apellido_y_nombre)

    def get_medico(self):
        entidad = "%s" % self.apellido_y_nombre.upper()
        if self.nro_doc:
            entidad = entidad + " - %s" % (self.nro_doc)
        if self.especialidad:
            entidad = entidad + " - %s" % (self.especialidad)
        return unicode(entidad.upper())


class ent_empresa(models.Model):
    razon_social = models.CharField(
        "Razón Social", max_length=200, blank=True, null=True
    )
    cuit = models.CharField("CUIT", max_length=50, blank=True, null=True)
    categFiscal = models.IntegerField(
        "Categoría Fiscal", choices=CATEG_FISCAL, blank=True, null=True
    )
    codigo = models.CharField("Código", max_length=50, blank=True, null=True)
    iibb = models.CharField("Nº IIBB", max_length=50, blank=True, null=True)
    fecha_inicio_activ = models.DateField(
        "Fecha Inicio Actividades", null=True, blank=True
    )
    domicilio = models.CharField("Domicilio", max_length=200, blank=True, null=True)
    provincia = models.IntegerField(
        "Provincia", choices=PROVINCIAS, blank=True, null=True, default=12
    )
    localidad = models.CharField("Localidad", max_length=100, blank=True, null=True)
    cod_postal = models.CharField("CP", max_length=50, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    telefono = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    celular = models.CharField("Celular", max_length=50, blank=True, null=True)
    baja = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_modif = models.DateTimeField(auto_now=True)
    usuario_carga = models.ForeignKey(
        "usuarios.UsuUsuario",
        db_column="usuario_carga",
        blank=True,
        null=True,
        related_name="empr_usuario_carga",
        on_delete=models.SET_NULL,
    )

    rubro = models.CharField("Rubro", max_length=200, blank=True, null=True)
    cant_empleados = models.IntegerField("Cant.Empl.", blank=True, null=True)
    art = models.ForeignKey(
        "ent_art",
        verbose_name="ART",
        db_column="art",
        blank=True,
        null=True,
        related_name="empr_art",
        on_delete=models.SET_NULL,
    )
    medico_prof = models.ForeignKey(
        "ent_medico_prof",
        verbose_name="Médico/Prof.",
        db_column="medico_prof",
        blank=True,
        null=True,
        related_name="empr_medico_prof",
        on_delete=models.SET_NULL,
    )

    casa_central = models.ForeignKey(
        "ent_empresa",
        verbose_name="Casa Central",
        db_column="casa_central",
        blank=True,
        null=True,
        related_name="empr_casa_central",
        on_delete=models.SET_NULL,
    )
    observaciones = models.TextField("Observaciones", blank=True, null=True)
    contacto_nombre = models.CharField("Nombre", max_length=200, blank=True, null=True)
    contacto_email = models.EmailField("Email", blank=True, null=True)
    contacto_tel = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    contacto_cargo = models.ForeignKey(
        "ent_cargo",
        verbose_name="Cargo",
        db_column="cargo",
        blank=True,
        null=True,
        related_name="empr_cargo",
        on_delete=models.SET_NULL,
    )
    contacto_profesion = models.ForeignKey(
        "ent_especialidad",
        verbose_name="Profesión",
        db_column="especialidad",
        blank=True,
        null=True,
        related_name="empr_especialidad",
        on_delete=models.SET_NULL,
    )

    agrupamiento = models.ForeignKey(
        "ent_empresa_agrupamiento",
        verbose_name="Agrupamiento/Gerencia Empresa",
        db_column="agrupamiento",
        blank=True,
        null=True,
        related_name="empr_agrupamiento",
        on_delete=models.SET_NULL,
    )

    objects = models.Manager()

    class Meta:
        db_table = "ent_empresa"
        ordering = ["razon_social", "cuit"]

    def __unicode__(self):
        return "%s" % unicode(self.razon_social.upper())

    def cantidad_empleados(self):
        empls = (
            ent_empleado.objects.filter(baja=False)
            .filter(Q(trab_fbaja__isnull=True) | Q(trab_fbaja__lt=hoy()))
            .select_related("empresa")
        )
        cant = 0
        # Si es sucursal
        if self.casa_central:
            cant = empls.filter(empresa=self).distinct().count()
        else:
            cant = (
                empls.filter(Q(empresa=self) | Q(empresa__casa_central=self))
                .distinct()
                .count()
            )
        return cant

    def get_empresa(self):
        entidad = "%s" % self.razon_social.upper()
        if not self.casa_central:
            entidad = "%s (EMPRESA/CASA CENTRAL)" % entidad
        return unicode(entidad.upper())

    def get_domicilio(self):
        domicilio = "%s" % self.domicilio
        if self.cod_postal:
            domicilio = "%s - CP:%s" % (domicilio, self.cod_postal)
        if self.localidad:
            domicilio = "%s - %s" % (domicilio, self.localidad)
        if self.provincia:
            domicilio = "%s - %s" % (domicilio, self.get_provincia_display())
        return unicode(domicilio.upper())


class ent_art(models.Model):
    codigo = models.CharField("Código", max_length=50, blank=True, null=True)
    # Field name made lowercase.
    nombre = models.CharField("Nombre", max_length=500, blank=True, null=True)
    prestador = models.CharField("Prestador", max_length=500, blank=True, null=True)
    auditor = models.CharField("Auditor", max_length=500, blank=True, null=True)
    contacto_nombre = models.CharField("Nombre", max_length=500, blank=True, null=True)
    contacto_telfijo = models.CharField(
        "Tel.Fijo", max_length=100, blank=True, null=True
    )
    contacto_telcel = models.CharField("Celular", max_length=100, blank=True, null=True)
    contacto_email = models.EmailField("Email", blank=True)
    baja = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modif = models.DateTimeField(auto_now=True)
    usuario_carga = models.ForeignKey(
        "usuarios.UsuUsuario",
        db_column="usuario_carga",
        blank=True,
        null=True,
        related_name="art_usuario_carga",
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "ent_art"
        ordering = [
            "nombre",
        ]

    def __unicode__(self):
        return "%s" % unicode(self.nombre)


# Tabla de la Base de Configuracion


class ent_empleado(models.Model):
    nro_doc = models.CharField("Documento", max_length=50, blank=True, null=True)
    legajo = models.CharField("Legajo", max_length=50, blank=True, null=True)
    apellido_y_nombre = models.CharField("Apelido y Nombre", max_length=200)
    fecha_nac = models.DateField("Fecha Nacimiento", blank=True, null=True)
    domicilio = models.CharField("Domicilio", max_length=200, blank=True, null=True)
    provincia = models.IntegerField(
        "Provincia", choices=PROVINCIAS, blank=True, null=True, default=12
    )
    localidad = models.CharField("Localidad", max_length=100, blank=True, null=True)
    cod_postal = models.CharField("CP", max_length=50, blank=True, null=True)
    email = models.EmailField("Email", blank=True)
    telefono = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    celular = models.CharField("Celular", max_length=50, blank=True, null=True)
    art = models.ForeignKey(
        "ent_art",
        verbose_name="ART",
        db_column="art",
        blank=True,
        null=True,
        related_name="empl_art",
        on_delete=models.SET_NULL,
    )

    empresa = models.ForeignKey(
        "ent_empresa",
        verbose_name="Empresa",
        db_column="empresa",
        blank=True,
        null=True,
        related_name="empl_empresa",
        on_delete=models.SET_NULL,
    )
    empr_fingreso = models.DateField("Fecha Ingreso", blank=True, null=True)
    trab_cargo = models.ForeignKey(
        "ent_cargo",
        verbose_name="Puesto de Trabajo",
        db_column="cargo",
        blank=True,
        null=True,
        related_name="empl_cargo",
        on_delete=models.SET_NULL,
    )
    trab_fingreso = models.DateField("Fecha Ingreso", blank=True, null=True)
    trab_fbaja = models.DateField("Fecha Baja", blank=True, null=True)

    trab_armas = models.CharField("¿Portación de Armas?", max_length=1, default="N")
    trab_tareas_dif = models.CharField("¿Tareas Diferentes?", max_length=1, default="N")
    trab_preocupac = models.CharField("¿Preocupacional?", max_length=1, default="N")
    trab_preocup_fecha = models.DateField("Fecha Preocupacional", blank=True, null=True)

    trab_preocup_conclus = models.TextField(
        "Conclusión Preocupacional", blank=True, null=True
    )
    trab_factores_riesgo = models.TextField(
        "Factores de Riesgo a lo que está Expuesto", blank=True, null=True
    )
    trab_tareas_dif_det = models.TextField(
        "Descripción Tareas Diferentes", blank=True, null=True
    )
    trab_anteriores = models.TextField("Trabajos Anteriores", blank=True, null=True)
    trab_antecedentes = models.TextField(
        "Antecedentes Patológicos", blank=True, null=True
    )
    trab_accidentes = models.TextField("Accidentes ART", blank=True, null=True)
    trab_vacunas = models.TextField("Vacunas", blank=True, null=True)

    observaciones = models.TextField("Otras Observaciones", blank=True, null=True)
    baja = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modif = models.DateTimeField(auto_now=True)
    usuario_carga = models.ForeignKey(
        "usuarios.UsuUsuario",
        db_column="usuario_carga",
        blank=True,
        null=True,
        related_name="empl_usuario_carga",
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "ent_empleado"
        ordering = ["apellido_y_nombre", "empresa", "nro_doc"]

    def __unicode__(self):
        return "%s" % (self.apellido_y_nombre)

    def save(self, *args, **kwargs):
        if self.apellido_y_nombre:
            self.apellido_y_nombre = self.apellido_y_nombre.upper()
        if self.domicilio:
            self.domicilio = self.domicilio.upper()

        super(ent_empleado, self).save()

    @property
    def get_edad(self):
        hoy = date.today()
        try:
            if self.fecha_nac:
                edad = relativedelta(hoy, self.fecha_nac).years
                return edad
            else:
                return 0
        except:
            return 0

    @property
    def get_antiguedad_trab(self):
        hasta = date.today()
        try:
            if self.trab_fingreso:
                if self.trab_fbaja:
                    hasta = self.trab_fbaja
                antig = relativedelta(hasta, self.trab_fingreso).years
                return antig
            else:
                return 0
        except:
            return 0

    @property
    def get_antiguedad_empr(self):
        hasta = date.today()
        try:
            if self.empr_fingreso:
                if self.trab_fbaja:
                    hasta = self.trab_fbaja
                antig = relativedelta(hasta, self.empr_fingreso).years
                return antig
            else:
                return 0
        except:
            return 0

    def get_empleado(self):
        entidad = "%s" % self.apellido_y_nombre.upper()
        if self.nro_doc:
            entidad = entidad + " - %s" % (self.nro_doc)
        if self.empresa:
            entidad = entidad + " - %s" % (self.empresa)
        return entidad.upper()

    def get_cargo(self):
        if self.trab_cargo:
            return unicode(self.trab_cargo.cargo)
        else:
            return ""

    def get_empresa(self):
        if self.empresa:
            return unicode(self.empresa.razon_social)
        else:
            return ""

    def get_art(self):
        if self.art:
            return unicode(self.art.nombre)
        else:
            return ""
