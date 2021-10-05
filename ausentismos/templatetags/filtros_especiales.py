# -*- coding: utf8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
@register.filter(name='proteger_dato')
def proteger_dato(value, permiso):
    if permiso:
        return value
    else:
        if not value or value == '':
            return value
        return mark_safe("<b>(NO DISPONIBLE)</b>")


