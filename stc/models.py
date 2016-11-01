import datetime
from datetime import datetime, date, timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)


def addworkdays(start, days, holidays=(), workdays=(MON, TUE, WED, THU, FRI)):
    # Definiendo funcion para agregar dias habiles a una fecha determinada
    weeks, days = divmod(days, len(workdays))
    result = start + timedelta(weeks=weeks)
    lo, hi = min(start, result), max(start, result)
    count = len([h for h in holidays if h >= lo and h <= hi])
    days += count * (-1 if days < 0 else 1)
    for _ in range(days):
        result += timedelta(days=1)
        while result in holidays or result.weekday() not in workdays:
            result += timedelta(days=1)
    return result


class Empresa(models.Model):
    # En este modelo usaremos una id como pk ya que solo son pocas empresas
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
    estado = models.BooleanField(default=True)
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
    fecha_radicacion = models.DateField()
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

    def tiene_gl(self):
        if Glosa.objects.filter(factura=self.factura):
            return "SI"
        else:
            return "NO"

    def fecha_max_glosa(self):
        fmg = addworkdays(self.fecha_radicacion, 20)
        return fmg


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
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Devolucion(models.Model):
    factura = models.CharField(max_length=20)
    empresa = models.ForeignKey(Empresa)
    unidad = models.ForeignKey(Unidad)
    convenio = models.ForeignKey(Convenio)
    fecha_devolucion = models.DateField()
    valor_factura = models.IntegerField()
    causal = models.ForeignKey(Causal)
    detalle = models.CharField(max_length=512)
    gestor = models.ForeignKey(Gestor)
    fecha_remitido = models.DateField(null=True)
    fecha_registro = models.DateField(null=True)
    gestion = models.CharField(max_length=512)
    fecha_gestion = models.DateField(null=True)
    estado = models.ForeignKey(EstadoDV)
    usuario = models.ForeignKey(User)
    fisico = models.BooleanField(default=True)

    def __str__(self):
        return self.factura + "@" + str(self.id)


class EstadoGL(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion


class Glosa(models.Model):
    factura = models.CharField(max_length=20)
    empresa = models.ForeignKey(Empresa)
    unidad = models.ForeignKey(Unidad)
    convenio = models.ForeignKey(Convenio)
    fecha_glosa = models.DateField()
    valor_factura = models.IntegerField()
    valor_glosa = models.IntegerField()
    saldo_glosa = models.PositiveIntegerField()
    causal = models.ForeignKey(Causal)
    fecha_max_respuesta = models.DateField()
    detalle = models.CharField(max_length=250)
    gestor = models.ForeignKey(Gestor)
    fecha_remitido = models.DateField(null=True)
    estado = models.ForeignKey(EstadoGL)
    fecha_ratificacion = models.DateField(null=True, blank=True)
    fecha_max_respuesta_rat = models.DateField(null=True, blank=True)
    fecha_registro = models.DateField(null=True)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.factura

    def extemporaneidad(self):
        fac = Radicacion.objects.get(factura=self.factura)
        fmg = fac.fecha_max_glosa()
        if self.fecha_glosa > fmg:
            return "SI"
        else:
            return "NO"

    def rat_extemporaneidad(self):
        fecha_max_ratificacion = addworkdays(self.fecha_respuesta, 10)
        if self.fecha_ratificacion > fecha_max_ratificacion:
            return "SI"
        else:
            return "NO"


class Respuesta(models.Model):
    fecha_respuesta = models.DateField()
    referencia = models.CharField(max_length=250, null=True)
    locked = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empresa)
    convenio = models.ForeignKey(Convenio)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return str(self.id)

    def procesada(self):
        if self.locked:
            return "Si"
        else:
            return "No"


class GlosaRespuesta(models.Model):
    glosa = models.OneToOneField(
        Glosa, on_delete=models.CASCADE, primary_key=True)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    gestion = models.CharField(max_length=512)
    aceptado_ips = models.IntegerField()
    codigo_respuesta = models.ForeignKey(Causal)
    fecha_registro = models.DateField(null=True)

    def __str__(self):
        return str(self.glosa)

    def no_aceptado(self):
        return int(self.glosa.valor_glosa) - int(self.aceptado_ips)


class GlosaRespRatif(models.Model):
    glosa = models.OneToOneField(
        Glosa, on_delete=models.CASCADE, primary_key=True)
    numero = models.IntegerField()
    fecha_respuesta = models.DateField()
    gestion = models.CharField(max_length=512)
    aceptado_ips = models.IntegerField()
    codigo_respuesta = models.ForeignKey(Causal)
    referencia = models.CharField(max_length=250, null=True)
    fecha_registro = models.DateField(null=True)

    def __str__(self):
        return str(self.glosa)


class GlosaActualizacion(models.Model):
    glosa = models.OneToOneField(
        Glosa, on_delete=models.CASCADE, primary_key=True)
    gestion = models.CharField(max_length=512)
    fecha_actualizacion = models.DateField()
    aceptado_ips = models.IntegerField()
    fecha_registro = models.DateField(null=True)
    usuario = models.ForeignKey(User)
