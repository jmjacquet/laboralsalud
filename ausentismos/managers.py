# -*- coding: utf-8 -*-
from django.db import models

class AusentismosActivos(models.Manager):
    def __init__(self):
        super(AusentismosActivos, self).__init__()

    def get_queryset(self):
        return super(AusentismosActivos, self).get_queryset().filter(baja=False)