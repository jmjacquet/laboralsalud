# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import  ausentismo,ausentismo_controles

# Register your models here.
admin.site.register(ausentismo)
admin.site.register(ausentismo_controles)