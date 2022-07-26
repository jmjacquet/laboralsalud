# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from laboralsalud.utilidades import *
from entidades.models import *
import datetime


class turnos(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    turno_empresa = models.ForeignKey(
        "entidades.ent_empresa",
        verbose_name="Empresa",
        db_column="empresa",
        blank=True,
        null=True,
        related_name="turno_empresa",
        on_delete=models.SET_NULL,
    )
    fecha = models.DateField("Fecha Turno", blank=True, null=True)
    hora = models.TimeField("Hora Turno", blank=True, null=True)
    turno_empleado = models.ForeignKey(
        "entidades.ent_empleado",
        verbose_name="Empleado",
        db_column="empleado",
        blank=True,
        null=True,
        related_name="turno_empleado",
        on_delete=models.SET_NULL,
    )
    detalle = models.CharField("Diagnóstico", max_length=100, blank=True, null=True)
    estado = models.IntegerField("Estado", choices=ESTADO_TURNO, blank=True, null=True)
    observaciones = models.TextField("Observaciones", blank=True, null=True)
    tipo_control = models.CharField("Tipo Control", choices=TIPO_CONTROL, max_length=1, blank=True, null=True)
    baja = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_modif = models.DateField(auto_now=True)
    usuario_carga = models.ForeignKey(
        "usuarios.UsuUsuario",
        db_column="usuario_carga",
        blank=True,
        null=True,
        related_name="turno_usuario_carga",
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "turnos"
        ordering = ["-fecha", "-hora", "estado"]

    def __unicode__(self):
        return "%s - %s" % (self.fecha.strftime("%d/%m/%Y"), self.turno_empleado)

    def get_turno(self):
        return "{0:0{width}}".format(self.pk, width=4)


class configuracion(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    nombre = models.CharField("Nombre", max_length=100)
    cuit = models.CharField("CUIT", max_length=50)
    iibb = models.CharField("Nº IIBB", max_length=50, blank=True, null=True)
    fecha_inicio_activ = models.DateField("Fecha Inicio Actividades", null=True)
    domicilio = models.CharField(
        "Domicilio/Ubicación", max_length=200, blank=True, null=True
    )
    datos_extra = models.CharField("Datos Extra", max_length=200, blank=True, null=True)

    mail_cuerpo = models.CharField(
        "Cuerpo del Email (envío de Ausentismos)", max_length=500, blank=True, null=True
    )
    mail_servidor = models.CharField("Servidor SMTP", max_length=100, blank=True)
    mail_puerto = models.IntegerField("Puerto", blank=True, null=True, default=587)
    mail_usuario = models.CharField("Usuario", max_length=100, blank=True)
    mail_password = models.CharField("Password", max_length=100, blank=True)

    # ruta_logo = models.ImageField(upload_to=get_image_name,db_column='ruta_logo', max_length=100,null=True, blank=True) # Field name made lowercase.
    ruta_logo = models.CharField(
        "Ruta Logo", db_column="ruta_logo", max_length=100, null=True, blank=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "configuracion"

    def __unicode__(self):
        return "%s" % (self.nombre)

    def get_datos_mail(self):
        from django.conf import settings

        d = {}
        d[
            "mensaje_inicial"
        ] = "Estimado/as les envío por este medio el informe correspondiente."
        d["mail_servidor"] = self.mail_servidor or settings.EMAIL_HOST
        d["mail_puerto"] = int(self.mail_puerto) or int(settings.EMAIL_PORT)
        d["mail_usuario"] = self.mail_usuario or settings.EMAIL_HOST_USER
        d["mail_password"] = self.mail_password or settings.EMAIL_HOST_PASSWORD
        d["mail_origen"] = (
            settings.DEFAULT_FROM_EMAIL or "contacto@sistemaslaboralsalud.com.ar"
        )
        d["mail_cuerpo"] = self.mail_cuerpo

        return d
