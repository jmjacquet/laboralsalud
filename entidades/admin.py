# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(ent_cargo)
admin.site.register(ent_especialidad)
admin.site.register(ent_empresa)
admin.site.register(ent_medico_prof)
admin.site.register(ent_art)
admin.site.register(ent_empleado)
