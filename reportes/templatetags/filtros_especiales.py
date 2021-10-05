# -*- coding: utf8 -*-
from django import template
from ausentismos.templatetags.filtros_especiales import proteger_dato
register = template.Library()

register.filter('proteger_dato', proteger_dato)

