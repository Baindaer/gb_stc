#importando modulos generales
import sqlite3
import os

#importando modulos de django
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import auth, messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
from django.contrib.auth.models import User

#importando modulos de aplicacion
from .models import *


def inicio(request):
    #Definiendo index de la pagina
    return render(request, 'stc/inicio.html',)

def login(request):
    #Definiendo la funcion iniciar sesion, validamos que se trate de un requerimiento tipo POST
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Usamos el metodo de autenticar de django para validar la informacion
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Contraseña correcta, se marca el usuario como activo
            auth.login(request, user)
            messages.success(request, 'Sesion iniciada correctamente')
            return HttpResponseRedirect(reverse('stc:inicio'))
        else:
            messages.error(request, 'Error de autenticación')
            return HttpResponseRedirect(reverse('stc:login'))
    else: 
        #Si no es un request tipo POST se renderiza la pagina de inicio de sesión
        return render(request, 'stc/login.html')

def logout(request):
    #Cerrando sesion
    auth.logout(request)
    messages.success(request, 'Sesión cerrada corretamente')
    return HttpResponseRedirect(reverse('stc:inicio'))

def radicacion(request):
    #Definiendo modulo de radicacion; iniciando por validar si existe una sesion activa
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Cargando variables de contexto iniciales
    last_registros = Radicacion.objects.order_by('-fecha_registro')[:40]
    empresas = Empresa.objects.all()
    convenios = Convenio.objects.all()
    servicios = Servicio.objects.all()
    context = {
        'last_registros':last_registros, 
        'empresas':empresas,
        'convenios':convenios,
        'servicios':servicios,
        }
    #Validando si es un get o un post
    if request.method == 'POST':
        #Agregando registro de radicacion
        factura = request.POST['factura'].upper()
        empresa = request.POST['empresa']
        convenio = request.POST['convenio'].upper()
        fecha_radicacion = request.POST['fecha_radicacion']
        valor_factura = request.POST['valor_factura']
        #Gestion de toogle
        try:
            tipo_contrato = request.POST['tipo_contrato']
        except:
            tipo_contrato = 0
        servicio = request.POST['servicio']
        mes_servicio = request.POST['mes_servicio']
        ref_unidad = empresa + factura[:2].upper()
        fecha_registro = timezone.now()
        #Validando datos de traidos del formulario
        try:
            convenio_id = Convenio.objects.get(nombre=convenio).nit
        except:
            messages.error(request, 'Convenio no existente')
            return render(request, 'stc/radicacion.html', context)
        try:
            unidad_id = RefUnidad.objects.get(referencia=ref_unidad).unidad_id
        except:
            messages.error(request, 'Unidad no existente para la combinacion de empresa y prefijo')
            return render(request, 'stc/radicacion.html', context)
        try:
            servicio_id=Servicio.objects.get(descripcion=servicio).id
        except:
            messages.error(request, 'Servicio no existente')
            return render(request, 'stc/radicacion.html', context)
        #Registro en la base de datos
        registro = Radicacion(
                factura=factura, 
                empresa_id=Empresa.objects.get(nombre=empresa).id, 
                convenio_id=convenio_id,
                unidad_id=unidad_id, 
                fecha_radicacion=fecha_radicacion, 
                valor_factura=valor_factura, 
                tipo_contrato=tipo_contrato, 
                servicio_id=servicio_id, 
                mes_servicio=mes_servicio, 
                fecha_registro=fecha_registro, 
                user_id=request.user.id,
                )
        registro.save()
        #Agregando datos a contexto
        context['pre_empresa'] = empresa
        context['pre_convenio'] = convenio
        context['pre_fecha_radicacion'] = fecha_radicacion
        messages.success(request, 'Factura ' + factura + ' registrada')
        return render(request, 'stc/radicacion.html', context)
    else:
        #Haciendo render con el contexto cargado
        return render(request, 'stc/radicacion.html', context)

def gestion_radicacion(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Cargando variables de contexto iniciales
    last_registros = Radicacion.objects.order_by('-fecha_registro')[:40]
    context = {
        'last_registros':last_registros, 
        }
    if request.method == 'POST':
        factura = request.POST['factura'].upper()
        if request.POST['submit'] == 'buscar':
            #Realizando filtro de consulta
            last_registros = Radicacion.objects.filter(factura__contains=factura).order_by('-fecha_registro')
            context['last_registros'] = last_registros
            print (last_registros)
            if last_registros:
                messages.success(request, 'Busqueda realizada')
            else:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/gestion_radicacion.html',context)
        if request.POST['submit'] == 'eliminar':
            #Eliminando registro
            try:
                exe = Radicacion.objects.get(factura=factura).delete()
                messages.success(request, 'Factura '+factura+' eliminada')
                last_registros = Radicacion.objects.order_by('-fecha_registro')[:40]
                context['last_registros'] = last_registros
            except:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/gestion_radicacion.html',context)
    else:
        return render(request, 'stc/gestion_radicacion.html',context)

def consulta(request):
    #Definiendo vista de consulta de factura
    if not request.user.is_authenticated:
        #Validando sesion
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    if request.method == 'POST':
        factura = request.POST['factura'].upper()  
        consulta_factura = Radicacion.objects.filter(factura=factura)
        if consulta_factura:
            messages.success(request, 'Busqueda realizada')
        else:
            messages.error(request, 'Factura no encontrada')
        context = {
        'consulta_factura':consulta_factura, 
        }
        return render(request, 'stc/consulta.html', context)
    return render(request, 'stc/consulta.html')

def reportes(request):
    return render(request, 'stc/reportes.html')

def reporte_capitas(request):
    if not request.user.is_authenticated:
        #Validando sesion
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Obteniendo las empresas unicas que en radicacion tiene al menos 1 registro como capita
    empresas = Empresa.objects.filter(radicacion__tipo_contrato='1').distinct()
    convenios = Convenio.objects.filter(radicacion__tipo_contrato='1').distinct()
    context = {
        'empresas':empresas,
        'convenios':convenios, 
        }
    if request.method == 'POST':
        empresa = request.POST['empresa']
        convenio = request.POST['convenio']
        mes_reporte = request.POST['mes_reporte']
        empresa_id = Empresa.objects.get(nombre=empresa).id,
        convenio_id = Convenio.objects.get(nombre=convenio).nit
        reporte_capitas = Radicacion.objects.filter(tipo_contrato='1', empresa=empresa_id, convenio=convenio_id, fecha_radicacion__startswith=mes_reporte )
        total_capitas = 0
        for each in reporte_capitas:
            total_capitas = total_capitas + each.valor_factura
        context['reporte_capitas'] = reporte_capitas
        context['total_capitas'] = total_capitas
        context['pre_empresa'] = empresa
        context['pre_convenio'] = convenio
        context['pre_mes_reporte'] = mes_reporte
        if reporte_capitas:
                messages.success(request, 'Reporte generado con exito')
        else:
            messages.error(request, 'Información no encontrada')
        return render(request, 'stc/reporte_capitas.html',context)

    return render(request, 'stc/reporte_capitas.html',context)