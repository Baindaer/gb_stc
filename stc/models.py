import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Empresa(models.Model):
    #En este modelo usaremos una id como pk ya que solo son pocas empresas
    id = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    nit = models.IntegerField()
    def __str__(self):
        return self.nombre

class Ejecutivo(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, null=True)
    def __str__(self):
        return self.id

class RefUnidad(models.Model):
    referencia = models.CharField(max_length=100, primary_key=True)
    unidad = models.ForeignKey(Unidad)
    def __str__(self):
        return self.referencia

class Convenio(models.Model):
    nit = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado =  models.BooleanField(default=True)
    ejecutivo = models.ForeignKey(Ejecutivo, null=True)
    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    descripcion = models.CharField(max_length=200)
    def __str__(self):
        return self.descripcion

class Radicacion(models.Model):
    factura = models.CharField(max_length=12, primary_key=True)
    empresa = models.ForeignKey(Empresa)
    unidad = models.ForeignKey(Unidad)
    convenio = models.ForeignKey(Convenio)
    fecha_radicacion = models.CharField(max_length=10)
    valor_factura = models.IntegerField()
    tipo_contrato = models.BooleanField(default=False)
    servicio = models.ForeignKey(Servicio, null=True)
    mes_servicio = models.CharField(max_length=7, null=True)
    usuario = models.ForeignKey(User)
    fecha_registro = models.DateTimeField(null=True)
    def __str__(self):
        return self.factura
    def contrato_tipo(self):
        if self.tipo_contrato == 1:
            return "CAPITA"
        else:
            return "EVENTO"
    def tiene_dev(self):
        if Devolucion.objects.filter(factura=self.factura):
            return "SI"
        else:
            return "NO"

class Causal(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=200)
    codigo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    grupo = models.CharField(max_length=100)
    def __str__(self):
        return self.codigo

class EstadoDV(models.Model):
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return self.descripcion

class Gestor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.nombre

class Devolucion(models.Model):
    factura = models.CharField(max_length=20)
    empresa = models.ForeignKey(Empresa)
    unidad = models.ForeignKey(Unidad)
    convenio = models.ForeignKey(Convenio)
    fecha_devolucion = models.CharField(max_length=10)
    valor_factura = models.IntegerField()
    causal = models.ForeignKey(Causal)
    detalle = models.CharField(max_length=250)
    gestor = models.ForeignKey(Gestor)
    fecha_remitido = models.CharField(max_length=10, null=True)
    fecha_registro = models.CharField(max_length=10, null=True)
    gestion = models.CharField(max_length=250)
    fecha_gestion = models.CharField(max_length=10, null=True)
    estado = models.ForeignKey(EstadoDV)
    usuario = models.ForeignKey(User)
    def __str__(self):
        return self.factura + "@" + self.fecha_devolucion
