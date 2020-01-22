# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import  turnos,configuracion

# Register your models here.
admin.site.register(turnos)
admin.site.register(configuracion)
