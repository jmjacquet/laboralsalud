# -*- coding: utf-8 -*-
from django.test import TestCase
from entidades import models
import datetime
from dateutil.relativedelta import relativedelta

import logging

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger("testing")


class TestEmpleadoModel(TestCase):
    """Test Empleado models CRUD"""

    def setUp(self):
        self.empleado = models.ent_empleado.objects.create(
            nro_doc="29387656",
            legajo=1,
            apellido_y_nombre="JUAN MANUEL JACQUET",
            email="jmjacquet@gmail.com",
            fecha_nac=datetime.date(1982, 05, 15),
        )

    def test_representation(self):
        """Test empleado unicode method"""
        empleado = models.ent_empleado.objects.get(nro_doc="29387656")
        self.assertEqual(self.empleado, empleado)
        self.assertEqual(self.empleado.__unicode__(), self.empleado.apellido_y_nombre)

    def test_get_edad(self):
        """Test empleado get_edad method"""
        age = relativedelta(datetime.datetime.now(), self.empleado.fecha_nac).years
        self.assertEqual(self.empleado.get_edad, age)

    def test_get_edad(self):
        """Test empleado get_edad method"""
        age = relativedelta(datetime.datetime.now(), self.empleado.fecha_nac).years
        self.assertEqual(self.empleado.get_edad, age)
