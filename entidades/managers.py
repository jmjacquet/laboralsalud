# -*- coding: utf-8 -*-
from django.db import models

# class EmpresasPermitidas(models.Manager):
#     def __init__(self, empresas):
#         super(EmpresasPermitidas, self).__init__()
#         self.empresas = empresas
#
#     def get_queryset(self):
#         return super(EmpresasPermitidas, self).get_queryset().filter(id__in=empresas)