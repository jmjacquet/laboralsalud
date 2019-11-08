# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

admin.site.register(UsuUsuario)
admin.site.register(UsuGrupo)
admin.site.register(UsuPermiso)
admin.site.register(UsuCategPermisos)

