#importando modulos generales
import csv
import os
import sqlite3
import json
from datetime import date, timedelta, datetime

#importando modulos de django
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum, Max
from django.contrib import auth, messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q

#importando modulos de aplicacion
from .models import *


def inicio(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('stc:login'))
    #Definiendo index de la pagina
    return render(request, 'stc/inicio.html',)

def login(request):
    #Definiendo la funcion iniciar sesion con un requerimiento POST
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
        #Si no es un request tipo POST se renderiza el login
        return render(request, 'stc/login.html')

def logout(request):
    #Cerrando sesion
    auth.logout(request)
    messages.success(request, 'Sesión cerrada corretamente')
    return HttpResponseRedirect(reverse('stc:inicio'))

def radicacion(request):
    #Definiendo modulo de radicacion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Cargando variables de contexto iniciales
    ult_reg = Radicacion.objects.order_by('-fecha_registro')[:40]
    context = {'ult_reg': ult_reg}
    return render(request, 'stc/radicacion.html', context)

def rad_agregar(request):
    #Validando si existe una sesion activa
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Cargando variables de contexto iniciales
    ult_reg = Radicacion.objects.order_by('-fecha_registro')[:40]
    empresas = Empresa.objects.all()
    convenios = Convenio.objects.all()
    servicios = Servicio.objects.all()
    context = {
        'ult_reg': ult_reg, 
        'empresas': empresas,
        'convenios': convenios,
        'servicios': servicios,
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
            return render(request, 'stc/rad_agregar.html', context)
        try:
            unidad_id = RefUnidad.objects.get(
                referencia=ref_unidad).unidad_id
        except:
            messages.error(request, 
                'Combinacion de empresa y prefijo no valida')
            return render(request, 'stc/rad_agregar.html', context)
        try:
            servicio_id=Servicio.objects.get(descripcion=servicio).id
        except:
            messages.error(request, 'Servicio no existente')
            return render(request, 'stc/rad_agregar.html', context)
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
                usuario_id=request.user.id,
                )
        registro.save()
        #Agregando datos a contexto
        context['pre_empresa'] = empresa
        context['pre_convenio'] = convenio
        context['pre_fecha_radicacion'] = fecha_radicacion
        messages.success(request, 'Factura ' + factura + ' registrada')
        return render(request, 'stc/rad_agregar.html', context)
    else:
        #Haciendo render con el contexto cargado
        return render(request, 'stc/rad_agregar.html', context)

def rad_gestion(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Cargando variables de contexto iniciales
    ult_reg = Radicacion.objects.order_by('-fecha_registro')[:50]
    context = {'ult_reg': ult_reg}
    if request.method == 'POST':
        factura = request.POST['factura'].upper()
        if request.POST['submit'] == 'buscar':
            #Realizando filtro de consulta
            ult_reg = Radicacion.objects.filter(
                factura__contains=factura
                ).order_by('-fecha_registro')[:100]
            context['ult_reg'] = ult_reg
            if ult_reg:
                messages.success(request, 'Busqueda realizada')
            else:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/rad_gestion.html', context)
        if request.POST['submit'] == 'eliminar':
            #Eliminando registro
            try:
                exe = Radicacion.objects.get(factura=factura).delete()
                messages.success(request, 
                    'Factura ' + factura + ' eliminada')
                ult_reg = Radicacion.objects.order_by(
                    '-fecha_registro')[:50]
                context['ult_reg'] = ult_reg
            except:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/rad_gestion.html', context)
    else:
        return render(request, 'stc/rad_gestion.html', context)

def consulta(request):
    #Definiendo vista de consulta de factura
    if not request.user.is_authenticated:
        #Validando sesion
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    if request.method == 'POST':
        factura = request.POST['factura'].upper()  
        data_factura = Radicacion.objects.filter(factura=factura)
        data_devolucion = Devolucion.objects.filter(factura=factura)
        if data_factura or data_devolucion:
            messages.success(request, 'Busqueda realizada')
        else:
            messages.error(request, 'Factura no encontrada')
        context = {
        'data_factura': data_factura, 
        'data_devolucion': data_devolucion,
        }
        return render(request, 'stc/consulta.html', context)
    return render(request, 'stc/consulta.html')

def reportes(request):
    return render(request, 'stc/reportes.html')

def rep_capitas(request):
    if not request.user.is_authenticated:
        #Validando sesion
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Obteniendo las empresas unicas que en radicacion tiene al 
    #menos 1 registro como capita
    empresas = Empresa.objects.filter(
        radicacion__tipo_contrato='1'
        ).distinct()
    convenios = Convenio.objects.filter(
        radicacion__tipo_contrato='1'
        ).distinct()
    context = {
        'empresas': empresas,
        'convenios': convenios, 
        }
    if request.method == 'POST':
        empresa = request.POST['empresa']
        convenio = request.POST['convenio']
        mes_reporte = request.POST['mes_reporte']
        empresa_id = Empresa.objects.get(nombre=empresa).id,
        convenio_id = Convenio.objects.get(nombre=convenio).nit
        reporte_capitas = Radicacion.objects.filter(
            tipo_contrato='1', 
            empresa=empresa_id, 
            convenio=convenio_id, 
            fecha_radicacion__startswith=mes_reporte,
            )
        val_dev = Devolucion.objects.filter(
            empresa=empresa_id, 
            convenio=convenio_id
            )
        context['pre_empresa'] = empresa
        context['pre_convenio'] = convenio
        context['pre_mes_reporte'] = mes_reporte
        if request.POST['submit'] == 'generar':
            if reporte_capitas:
                messages.success(request, 'Reporte generado con exito')
            else:
                messages.error(request, 'Información no encontrada')
                return render(request, 'stc/rep_capitas.html', context)
            total_capitas = 0
            for each in reporte_capitas:
                total_capitas = total_capitas + each.valor_factura
            context['reporte_capitas'] = reporte_capitas
            context['val_dev'] = val_dev
            context['total_capitas'] = total_capitas
            return render(request, 'stc/rep_capitas.html', context)
        if request.POST['submit'] == 'exportar':
            if reporte_capitas:
                response = HttpResponse(content_type='text/csv')
                #Asignando nombre de archivo
                header = 'attachment; filename="reporte_capitas.csv"'
                response['Content-Disposition'] = header
                #Creando el archivo csv con el tipo de delimitador ; semicolon
                #para ser leido por excel
                writer = csv.writer(response, delimiter=';')
                #Escribiendo archivo, el proceso puede tardar varios segundos
                writer.writerow([
                    'Factura', 
                    'Convenio', 
                    'Radicado', 
                    'Servicio', 
                    'Tiene_Dev', 
                    'Valor'
                    ])
                for each in reporte_capitas:
                    writer.writerow([
                        each.factura, 
                        each.convenio.nombre, 
                        each.fecha_radicacion, 
                        each.servicio.descripcion, 
                        each.tiene_dev(), 
                        each.valor_factura
                        ])
                return response
            else:
                messages.error(request, 'Información no encontrada')
                return render(request, 'stc/rep_capitas.html', context)
    return render(request, 'stc/rep_capitas.html', context)

def rep_dev_revision(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    pass

def devoluciones(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    ult_reg = Devolucion.objects.order_by('-id')[:40]
    fecha = timezone.now()
    mes_actual = fecha.month
    dev = Devolucion.objects.all()
    dev_mes = Devolucion.objects.filter(fecha_devolucion__month=mes_actual)
    cant_dv_reg = dev_mes.count()
    vr_dv_reg = dev_mes.aggregate(
        Sum('valor_factura')
        )['valor_factura__sum'] / 1000000
    cant_dv_registradas = dev.filter(estado=1).count()
    cant_dv_revision = dev.filter(estado=2).count()
    context = {
        'ult_reg': ult_reg,
        'cant_dv_reg': cant_dv_reg,
        'vr_dv_reg': "%.0f" % vr_dv_reg,
        'fecha': fecha,
        'cant_dv_registradas':cant_dv_registradas,
        'cant_dv_revision': cant_dv_revision,
        }
    return render(request, 'stc/devoluciones.html', context)

def dev_agregar(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    ult_reg = Devolucion.objects.order_by('-id')[:40]
    empresas = Empresa.objects.all()
    convenios = Convenio.objects.all()
    causales = Causal.objects.all()
    gestores = Gestor.objects.all()
    radicacion = Radicacion.objects.all()
    context = {
        'ult_reg': ult_reg,
        'empresas': empresas,
        'convenios': convenios,
        'causales': causales,
        'gestores': gestores,
        'radicacion': radicacion,
        }
    if request.method == 'POST':
        factura = request.POST['factura'].upper()
        empresa = request.POST['empresa']
        convenio = request.POST['convenio']
        fecha_devolucion = request.POST['fecha_devolucion']
        valor_factura = request.POST['valor_factura']
        causal = request.POST['causal']
        detalle = request.POST['detalle'].upper()
        gestor = request.POST['gestor']
        ref_unidad = empresa + factura[:2].upper()
        fecha_registro = timezone.now()
        #Validando datos de traidos del formulario
        try:
            convenio_id = Convenio.objects.get(nombre=convenio).nit
        except:
            messages.error(request, 'Convenio no existente')
            return render(request, 'stc/dev_agregar.html', context)
        try:
            unidad_id = RefUnidad.objects.get(referencia=ref_unidad).unidad_id
        except:
            messages.error(request, 
                'Combinacion de empresa y prefijo no valida')
            return render(request, 'stc/dev_agregar.html', context)
        try:
            gestor_id=Gestor.objects.get(nombre=gestor).id
        except:
            messages.error(request, 'Gestor no existente')
            return render(request, 'stc/dev_agregar.html', context)
        try:
            causal_id = Causal.objects.get(codigo=causal).id
        except:
            messages.error(request, 'Causal no existente')
            return render(request, 'stc/dev_agregar.html', context)
        #Registro en la base de datos 
        registro = Devolucion(
                factura=factura, 
                empresa_id=Empresa.objects.get(nombre=empresa).id, 
                convenio_id=convenio_id,
                unidad_id=unidad_id, 
                fecha_devolucion=fecha_devolucion, 
                valor_factura=valor_factura,  
                fecha_registro=fecha_registro, 
                usuario_id=request.user.id,
                causal_id=causal_id,
                detalle=detalle,
                gestor_id=gestor_id,
                estado_id="1",
                )
        registro.save()
        #Cargando datos de contexto
        context['pre_empresa'] = empresa
        context['pre_convenio'] = convenio
        messages.success(request, 
            'Devolución de la factura ' + factura + ' registrada')
        return render(request, 'stc/dev_agregar.html', context)
    return render(request, 'stc/dev_agregar.html', context)

def dev_gestion(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #Cargando variables de contexto iniciales
    ult_reg = Devolucion.objects.order_by('-id')[:50]
    context = {'ult_reg': ult_reg}
    if request.method == 'POST':
        factura = request.POST['factura'].upper()
        id_registro = request.POST['id_registro']
        if request.POST['submit'] == 'buscar':
            #Realizando filtro de consulta
            ult_reg = Devolucion.objects.filter(
                factura__contains=factura
                ).order_by('-id')[:100]
            context['ult_reg'] = ult_reg
            if ult_reg:
                messages.success(request, 'Busqueda realizada')
            else:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/dev_gestion.html',context)
        if request.POST['submit'] == 'eliminar':
            #Eliminando registro
            try:
                exe = Devolucion.objects.get(id=id_registro).delete()
                messages.success(request, 
                    'Devolucion de ' + factura + ' eliminada')
                ult_reg = Devolucion.objects.order_by('-id')[:50]
                context['ult_reg'] = ult_reg
            except:
                messages.error(request, 
                    'Factura no seleccionada')
            return render(request, 'stc/dev_gestion.html', context)
    else:
        return render(request, 'stc/dev_gestion.html', context)

def exportar(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = '''
        attachment; filename="somefilename.csv"'''
    capita = Radicacion.objects.filter(tipo_contrato='1', empresa="GB")
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Factura', 'Valor', 'EPS', 'Fecha de radicacion'])
    for each in capita:
        writer.writerow([
            each.factura,
            each.valor_factura,
            each.convenio.nombre,
            each.fecha_radicacion
            ])
    return response

def exp_rad_general(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    #definiendo el tipo de response a texto o csv
    response = HttpResponse(content_type='text/csv')
    #Asignando nombre de archivo
    response['Content-Disposition'] = 'attachment; filename="radicacion.csv"'
    #Consultando base de datos
    data = Radicacion.objects.filter(fecha_radicacion__startswith='2016')
    #data = Radicacion.objects.all()
    #Creando el archivo csv con el tipo de delimitador ; para excel
    writer = csv.writer(response, delimiter=';')
    #Escribiendo archivo, el proceso puede tardar varios segundos
    writer.writerow([
        'Factura', 
        'Convenio', 
        'Unidad', 
        'Tipo contrato', 
        'Valor', 
        'Fecha Radicacion',
        'Mes Servicio',
        ])
    for each in data:
        writer.writerow([
            each.factura, 
            each.convenio, 
            each.unidad, 
            each.contrato_tipo(), 
            each.valor_factura, 
            each.fecha_radicacion,
            each.mes_servicio,
            ])
    return response

def pruebas(request):
    context = {}
    messages.success(request, 'probando 1,2,3')
    print (messages)
    return render(request, 'stc/pruebas.html', context)

def dev_remision(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    gestores = Gestor.objects.all()
    context = {'gestores':gestores}
    if request.method == 'POST':
        if request.POST['submit'] == 'buscar':
            #Realizando filtro de consulta
            gestor = request.POST['gestor']
            try:
                gestor_id = Gestor.objects.get(nombre=gestor).id
            except:
                messages.error(request, 'Gestor no existente')
                return render(request, 'stc/dev_remision.html', context)
            pendientes = Devolucion.objects.filter(
                gestor_id=gestor_id, 
                estado="1"
                ).order_by('-id')
            context['pendientes'] = pendientes
            context['gestor'] = gestor
            if pendientes:
                messages.success(request, 'Devoluciones pendientes mostradas')
            else:
                messages.error(request, 
                    'El gestor no tiene devoluciones por remitir')
            return render(request, 'stc/dev_remision.html', context)
        if request.POST['submit'] == 'remitir':
            #Realizando filtro de consulta
            gestor = request.POST['gestor']
            try:
                gestor_id = Gestor.objects.get(nombre=gestor).id
            except:
                messages.error(request, 'Gestor no existente')
                return render(request, 'stc/dev_remision.html', context)
            pendientes = Devolucion.objects.filter(
                gestor_id=gestor_id, 
                estado="1"
                ).order_by('-id')
            gestor_id= Gestor.objects.get(nombre=gestor)
            if pendientes:
                #Realizando realmente la remision luego de las validaciones
                fecha_actual = timezone.now()
                fecha_remitido = fecha_actual.strftime('%Y-%m-%d')
                context['fecha'] = fecha_actual
                context['pendientes'] = pendientes
                context['gestor'] = gestor
                subject = 'Notificación de devolución'
                from_email = 'notificaciones.carteragb@gmail.com'
                emails = gestor_id.email
                c = emails.count(",") + 1
                to = []
                start = 0
                if c == 1:
                    to = [emails]
                else:
                    for i in range (c):
                        u = emails.find(",",start)
                        if start == 0:
                            s = emails[ start : start + u ]
                        else:
                            s = emails[ start + 2*i : start + u + 2*i]
                        start += u 
                        to.append(s)
                to.append('cartera@gestionarbienestar.com')
                html_content = render_to_string(
                    'stc/dev_rem_email.html', context)
                # Esto desnuda el contenido del html para ser leido desde
                # cualquier cliente de correo sin soporte html
                text_content = strip_tags(html_content) 
                # Creando el correo.
                msg = EmailMultiAlternatives(
                    subject, 
                    text_content, 
                    from_email, 
                    to
                    )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                for each in pendientes:
                    #Actualizando estados
                    mod = Devolucion.objects.get(id=each.id)
                    mod.estado_id = "2"
                    mod.fecha_remitido = fecha_remitido
                    mod.save() 
                return render(request, 'stc/dev_rem_email.html', context)           
            else:
                messages.error(request, 
                    'El gestor no tiene devoluciones para remitir')
            return render(request, 'stc/dev_remision.html', context)
    return render(request, 'stc/dev_remision.html', context)

def dev_actualizacion(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    ult_reg = Devolucion.objects.order_by('-id')[:50]
    estados = EstadoDV.objects.all()
    context = {
        'ult_reg':ult_reg, 
        'estados':estados,
        }
    if request.method == 'POST':
        factura = request.POST['factura'].upper()
        id_registro = request.POST['id_registro']
        if request.POST['submit'] == 'buscar':
            #Realizando filtro de consulta
            ult_reg = Devolucion.objects.filter(
                factura__contains=factura
                ).order_by('-id')[:100]
            context['ult_reg'] = ult_reg
            if ult_reg:
                messages.success(request, 'Busqueda realizada')
            else:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/dev_actualizacion.html', context)
        if request.POST['submit'] == 'actualizar':
            estado = request.POST['estado'].upper()
            fecha_gestion = request.POST['fecha_gestion']
            gestion = request.POST['gestion'].upper()
            estado_id = EstadoDV.objects.get(descripcion=estado)
            #Actualizando registro
            try:
                mod = Devolucion.objects.get(id=id_registro)
                mod.estado_id = estado_id
                mod.fecha_gestion = fecha_gestion
                if gestion != "":
                    mod.gestion = gestion
                mod.save()
                messages.success(request, 'La devolucion ha sido actualizada')
                ult_reg = Devolucion.objects.order_by('-id')[:50]
                context['ult_reg'] = ult_reg
            except:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/dev_actualizacion.html', context)
    else:
        return render(request, 'stc/dev_actualizacion.html', context)

def glosas(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    ult_reg = Glosa.objects.order_by('-id')[:50]
    context = {'ult_reg':ult_reg}
    return render(request, 'stc/glosas.html', context)

def gl_agregar(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    ult_reg = Glosa.objects.order_by('-id')[:50]
    empresas = Empresa.objects.all()
    convenios = Convenio.objects.all()
    causales = Causal.objects.all()
    gestores = Gestor.objects.all()
    context = {
        'ult_reg':ult_reg,
        'empresas':empresas,
        'convenios':convenios,
        'causales':causales,
        'gestores':gestores,
        }
    if request.method == 'POST':
        factura = request.POST['factura'].upper()
        empresa = request.POST['empresa']
        convenio = request.POST['convenio']
        fecha_glosa = request.POST['fecha_glosa']
        valor_factura = request.POST['valor_factura']
        valor_glosa = request.POST['valor_glosa']
        causal = request.POST['causal']
        detalle = request.POST['detalle'].upper()
        gestor = request.POST['gestor']
        ref_unidad = empresa + factura[:2].upper()
        fecha_registro = timezone.now()
        #Validando datos de traidos del formulario
        try:
            convenio_id = Convenio.objects.get(nombre=convenio).nit
        except:
            messages.error(request, 'Convenio no existente')
            return render(request, 'stc/gl_agregar.html', context)
        try:
            unidad_id = RefUnidad.objects.get(referencia=ref_unidad).unidad_id
        except:
            messages.error(request, 
                'Combinacion de empresa y prefijo no valida')
            return render(request, 'stc/gl_agregar.html', context)
        try:
            gestor_id=Gestor.objects.get(nombre=gestor).id
        except:
            messages.error(request, 'Gestor no existente')
            return render(request, 'stc/gl_agregar.html', context)
        try:
            causal_id = Causal.objects.get(codigo=causal).id
        except:
            messages.error(request, 'Causal no existente')
            return render(request, 'stc/gl_agregar.html', context)
        #Registro en la base de datos 
        registro = Glosa(
                factura=factura, 
                empresa_id=Empresa.objects.get(nombre=empresa).id, 
                convenio_id=convenio_id,
                unidad_id=unidad_id, 
                fecha_glosa=fecha_glosa,
                #Agregando 20 días habiles a la conversion de 
                #fecha_glosa a dato tipo date con strp
                fecha_max_respuesta=addworkdays(
                    datetime.strptime(fecha_glosa, '%Y-%m-%d').date(), 20),
                valor_factura=valor_factura, 
                valor_glosa=valor_glosa,
                saldo_glosa=valor_glosa,
                fecha_registro=fecha_registro, 
                usuario_id=request.user.id,
                causal_id=causal_id,
                detalle=detalle,
                gestor_id=gestor_id,
                estado_id="1",
                )
        registro.save()
        #Cargando datos de contexto
        context['pre_empresa'] = empresa
        context['pre_convenio'] = convenio
        messages.success(request, 
            'Glosa de la factura ' + factura + ' registrada')
        return render(request, 'stc/gl_agregar.html', context)
    return render(request, 'stc/gl_agregar.html', context)

def gl_gestion(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    ult_reg = Glosa.objects.order_by('-id')[:50]
    context = {'ult_reg':ult_reg}
    if request.method == 'POST':
        factura = request.POST['factura'].upper()
        id_registro = request.POST['id_registro']
        if request.POST['submit'] == 'buscar':
            #Realizando filtro de consulta
            ult_reg = Glosa.objects.filter(
                factura__contains=factura
                ).order_by('-id')[:100]
            context['ult_reg'] = ult_reg
            if ult_reg:
                messages.success(request, 'Busqueda realizada')
            else:
                messages.error(request, 'Factura no encontrada')
            return render(request, 'stc/gl_gestion.html', context)
        if request.POST['submit'] == 'eliminar':
            #Eliminando registro
            try:
                exe = Glosa.objects.get(id=id_registro).delete()
                messages.success(request, 
                    'Glosa de la factura ' + factura + ' ha sido eliminada')
                ult_reg = Glosa.objects.order_by('-id')[:50]
                context['ult_reg'] = ult_reg
            except:
                messages.error(request, 'Factura seleccionada')
            return render(request, 'stc/gl_gestion.html',context)
    else:
        return render(request, 'stc/gl_gestion.html',context)

def get_factura(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    if request.method == 'POST':
        factura = request.POST.get('factura').upper()
        rad = Radicacion.objects.get(factura=factura)
        empresa = rad.empresa.nombre
        convenio = rad.convenio.nombre
        valor_factura = rad.valor_factura
        servicio = rad.servicio.descripcion
        fecha_radicacion = rad.fecha_radicacion.strftime('%Y-%m-%d')
        tipo_contrato = rad.tipo_contrato
        mes_servicio = rad.mes_servicio
        data = {
            'empresa': empresa,
            'convenio':convenio,
            'valor_factura': valor_factura,
            'servicio': servicio,
            'fecha_radicacion': fecha_radicacion,
            'tipo_contrato': tipo_contrato,
            'mes_servicio': mes_servicio,
            }
        return HttpResponse(json.dumps(data), content_type='application/json')
    pass

def get_glosa(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    if request.method == 'POST':
        glosa = request.POST.get('glosa')
        gl = Glosa.objects.get(id=glosa)
        valor_glosa = gl.valor_glosa
        factura = gl.factura
        try:
            extemporaneidad = gl.extemporaneidad()
        except:
            extemporaneidad = "NO"
        data = {
            'valor_glosa': valor_glosa,
            'factura': factura,
            'extemporaneidad': extemporaneidad,
            }
        return HttpResponse(json.dumps(data), content_type='application/json')
    pass

def get_respuesta(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        resp = Respuesta.objects.filter(numero=respuesta)[:1]
        for each in resp:
            gl = Glosa.objects.get(id=each.glosa_id)
            convenio = gl.convenio.nombre
            empresa = gl.empresa.nombre
            cerrado = each.cerrado
            fecha_respuesta = each.fecha_respuesta.strftime('%Y-%m-%d')
            referencia = each.referencia
        data = {
            'convenio': convenio,
            'empresa': empresa,
            'cerrado': cerrado,
            'fecha_respuesta': fecha_respuesta,
            'referencia': referencia,
            }
        return HttpResponse(json.dumps(data), content_type='application/json')
    pass

def gl_remision(request):
    #Validando sesion
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    gestores = Gestor.objects.all()
    context = {'gestores': gestores}
    if request.method == 'POST':
        if request.POST['submit'] == 'buscar':
            #Realizando filtro de consulta
            gestor = request.POST['gestor']
            try:
                gestor_id = Gestor.objects.get(nombre=gestor).id
            except:
                messages.error(request, 'Gestor no existente')
                return render(request, 'stc/gl_remision.html', context)
            pendientes = Glosa.objects.filter(
                gestor_id=gestor_id, 
                estado="1",
                ).order_by('-id')
            context['pendientes'] = pendientes
            context['gestor'] = gestor
            if pendientes:
                messages.success(request, 'Glosas pendientes mostradas')
            else:
                messages.error(request, 
                    'El gestor no tiene glosas para remitir')
            return render(request, 'stc/gl_remision.html',context)
        if request.POST['submit'] == 'remitir':
            #Realizando filtro de consulta
            gestor = request.POST['gestor']
            try:
                gestor_id = Gestor.objects.get(nombre=gestor).id
            except:
                messages.error(request, 'Gestor no existente')
                return render(request, 'stc/gl_remision.html', context)
            pendientes = Glosa.objects.filter(
                gestor_id=gestor_id, estado="1").order_by('-id')
            gestor_id= Gestor.objects.get(nombre=gestor)
            if pendientes:
                #Realizando realmente la remision luego de las validaciones
                fecha_actual = timezone.now()
                fecha_remitido = fecha_actual.strftime('%Y-%m-%d')
                context['fecha'] = fecha_actual
                context['pendientes'] = pendientes
                context['gestor'] = gestor
                subject = 'Notificación de glosa'
                from_email = 'notificaciones.carteragb@gmail.com'
                to = gestor_id.email
                html_content = render_to_string(
                    'stc/gl_rem_email.html', context)
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(
                    subject, 
                    text_content, 
                    from_email, 
                    [to]
                    )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                for each in pendientes:
                    #Actualizando estados
                    mod = Glosa.objects.get(id=each.id)
                    mod.estado_id = "2"
                    mod.fecha_remitido = fecha_remitido
                    mod.save() 
                return render(request, 'stc/gl_rem_email.html', context)           
            else:
                messages.error(request, 
                    'El gestor no tiene devoluciones para remitir')
    return render(request, 'stc/gl_remision.html', context)

def gl_resp_agregar(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    convenios = Convenio.objects.all().order_by('nombre')
    empresas = Empresa.objects.all()
    ult_respuesta = Respuesta.objects.order_by('-id')[0]
    new_respuesta = int(ult_respuesta.id) + 1
    context = {
        'new_respuesta': new_respuesta,
        'convenios': convenios,
        'empresas': empresas,
        }
    if request.method == 'POST':
        respuesta = request.POST['respuesta']
        if request.POST['submit'] == 'respuesta_cons':
            try:
                dat_resp = Respuesta.objects.get(id=respuesta)
            except:
                messages.error(request, 'Respuesta no existente')
                return HttpResponseRedirect(reverse('stc:gl_resp_agregar'))
            convenio = dat_resp.convenio.nombre
            empresa = dat_resp.empresa.nombre
            referencia = dat_resp.referencia
            fecha_respuesta = dat_resp.fecha_respuesta.strftime('%Y-%m-%d')
            print(fecha_respuesta)
            detallados = GlosaRespuesta.objects.filter(respuesta=respuesta)
            context['pre_respuesta'] = respuesta
            context['pre_empresa'] = empresa
            context['pre_convenio'] = convenio
            context['pre_referencia'] = referencia
            context['pre_fecha_respuesta'] = fecha_respuesta
            context['detallados'] = detallados
            context['band_detalle'] = True
            glosas = Glosa.objects.filter(
            estado="2",
            convenio_id=Convenio.objects.get(nombre=convenio).nit,
            empresa_id=Empresa.objects.get(nombre=empresa).id
            )
            context['glosas'] = glosas
            return render(request, 'stc/gl_resp_agregar.html', context)
        empresa = request.POST['empresa']
        convenio = request.POST['convenio'].upper()
        referencia = request.POST['referencia']
        fecha_respuesta = request.POST['fecha_respuesta']
        try:
            convenio_id = Convenio.objects.get(nombre=convenio).nit
        except:
            messages.error(request, 'Convenio no existente')
            return render(request, 'stc/gl_resp_agregar.html', context)
        context['pre_empresa'] = empresa
        context['pre_convenio'] = convenio
        context['pre_referencia'] = referencia
        context['pre_fecha_respuesta'] = fecha_respuesta
        context['band_detalle'] = True
        glosas = Glosa.objects.filter(
            estado="2",
            convenio_id=convenio_id,
            empresa_id=Empresa.objects.get(nombre=empresa).id
            )
        context['glosas'] = glosas
        if request.POST['submit'] == 'respuesta_reg':
            registro = Respuesta(
                empresa_id=Empresa.objects.get(nombre=empresa).id, 
                convenio_id=convenio_id,
                referencia=referencia,
                fecha_respuesta=fecha_respuesta,
                locked=False,
                )
            registro.save()
            context['pre_respuesta'] = Respuesta.objects.order_by('-id')[0]
            messages.success(request, 
                'Respuesta #' + str(context['pre_respuesta']) + ' registrada')
            return render(request, 'stc/gl_resp_agregar.html', context)
        if request.POST['submit'] == 'respuesta_det':
            glosa = request.POST['glosa']
            gestion = request.POST['gestion']
            aceptado_ips = request.POST['aceptado_ips']
            fecha_registro = timezone.now()
            valor_factura = Glosa.objects.get(id=glosa).valor_factura  
            if valor_factura == aceptado_ips:
                codigo_respuesta = "997"
            elif aceptado_ips == 0:
                codigo_respuesta = "999"
            else:
                codigo_respuesta = "998"
            saldo_glosa = Glosa.objects.get(id=glosa).saldo_glosa 
            if saldo_glosa < int(aceptado_ips):
                context['pre_respuesta'] = Respuesta.objects.order_by('-id')[0]
                messages.success(request,'El valor aceptado supera al saldo de la glosa')
                return render(request, 'stc/gl_resp_agregar.html', context)
            registro = GlosaRespuesta(
                glosa=Glosa.objects.get(id=glosa),
                respuesta_id=respuesta,
                gestion=gestion,
                aceptado_ips=aceptado_ips,
                codigo_respuesta_id=codigo_respuesta,
                fecha_registro=fecha_registro,
                )
            registro.save()
            actualizacion = Glosa.objects.get(id=glosa)
            actualizacion.estado_id = "3"
            actualizacion.save()
            context['pre_respuesta'] = Respuesta.objects.order_by('-id')[0]
            detallados = GlosaRespuesta.objects.filter(respuesta=respuesta)
            context['detallados'] = detallados
            return render(request, 'stc/gl_resp_agregar.html', context)

    return render(request, 'stc/gl_resp_agregar.html', context)

def gl_respuestas(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe iniciar sesion primero.')
        return HttpResponseRedirect(reverse('stc:login'))
    context = {}
    ult_reg = Respuesta.objects.all()
    return render(request, 'stc/gl_respuestas.html', context)
