# -*- coding: utf-8 -*-
from django.db import models


class CasasCentrales(models.Manager):
    def __init__(self):
        super(CasasCentrales, self).__init__()

    def get_queryset(self):
        return super(CasasCentrales, self).get_queryset().filter(baja=False, casa_central__isnull=False)


class Sucursales(models.Manager):
    def __init__(self):
        super(Sucursales, self).__init__()

    def get_queryset(self):
        return super(Sucursales, self).get_queryset().filter(baja=False, casa_central__isnull=False)