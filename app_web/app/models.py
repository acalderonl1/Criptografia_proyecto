# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Credenciales(models.Model):
    plataforma = models.CharField(max_length=400, verbose_name="plataforma")
    usuario = models.CharField(max_length=300, verbose_name="usuario")
    contrasena = models.CharField(max_length=200, verbose_name="contrasena")
    fecha_creacion = models.DateTimeField(verbose_name='Fecha de creacion', null=True)
