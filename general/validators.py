# -*- coding: utf-8 -*-
from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models
from django.core.exceptions import ValidationError


# creating a validator function
def validar_fecha_nacimiento(value):
    hoy = date.today()
    if value:
        if value >= hoy:
            raise ValidationError(u"Verifique que la fecha sea válida")
        edad = relativedelta(hoy, value).years
        if edad < 18:
            raise ValidationError(u"El empleado no puede ser menor de 18 años")
        else:
            return value
    else:
        raise ValidationError(u"Verifique que la fecha sea válida")
