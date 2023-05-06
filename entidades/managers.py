# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

from laboralsalud.utilidades import hoy


class EmpleadosActivos(models.Manager):
    def __init__(self):
        super(EmpleadosActivos, self).__init__()

    def get_queryset(self):
        return (
            super(EmpleadosActivos, self)
            .get_queryset()
            .filter(baja=False)
        )
