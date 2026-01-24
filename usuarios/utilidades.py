from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from laboralsalud.utilidades import usuario_actual, empresa_y_sucursales
from usuarios.models import UsuPermiso

@login_required
def ver_permisos(request):
    try:
        if request:
            usuario = usuario_actual(request)
            if usuario.tipoUsr == 0:
                permisos = UsuPermiso.objects.all().values_list('permiso_name', flat=True).distinct()
            else:
                # permisos = UsuPermiso.objects.filter(grupo=usuario.grupo).values_list('permiso_name', flat=True).distinct()
                permisos = usuario.permisos.values_list('permiso_name', flat=True).distinct()
        else:
            permisos = []
    except:
        permisos = []

    return permisos


@login_required
def tiene_permiso(request, permiso):
    permisos = ver_permisos(request)
    return (permiso in permisos)


def tiene_empresa(usuario, empresa):
    if usuario:
        if usuario.tipoUsr == 0:
            return True
        else:
            if empresa:
                empr_elegidas = empresa_y_sucursales(empresa.id)
                usr_empresas = usuario.empresas.values_list('id', flat=True).distinct()
                return any(e in usr_empresas for e in empr_elegidas)
            else:
                return False
    return False


# @login_required
def password(request):
    if request.method == 'GET':
        clave = request.GET.get('clave', '')
        if clave:
            clave = make_password(password=clave, salt=None)

    return HttpResponse(clave, content_type='application/json')


def unpassword(request):
    if request.method == 'GET':
        clave = request.GET.get('clave', '')
        if clave:
            clave = make_password(password=clave, salt=None)

    return HttpResponse(clave, content_type='application/json')