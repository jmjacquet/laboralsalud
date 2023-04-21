# -*- coding: utf-8 -*-
from datetime import datetime, timedelta,date
import calendar

TIPO_USR = (
    (0, u'Administrador'),
    (1, u'Médico/Profesional'),
    (2, u'RRHH/Empresa'),
)

TIPO_ENTIDAD = (    
    (1, 'Cliente'),
    (2, 'Proveedor'),
    (3, 'Empleado'),
)

TIPO_AUSENCIA = (
    (1, 'Inculpable'),    
    (2, 'Accidente Denunciado'),
    (7, 'Accidente No Denunciado'),
    (4, 'Familiar Enfermo'),
    (5, 'Licencias Especiales'),
    (6, 'Embarazo'),
    (8, 'Consulta/Control rutinario'),
)

TIPO_AUSENCIA_MEDICOS = (
    (1, 'Inculpable'),
    (3, 'Enfermedad Profesional'),
    (2, 'Accidente Denunciado'),
    (7, 'Accidente No Denunciado'),    
    (4, 'Familiar Enfermo'),
    (8, 'Consulta/Control rutinario'),
)

TIPO_CONTROL = (
    ('', '----'),
    ('C', 'Consultorio'),
    ('S', 'Consultorio CIBYS'),
    ('D', u'Control Telefónico'),
    ('E', u'Evolución ART'),
    ('R', u'Otros Registros'),
    ('V', u'Visita a Domicilio'),
)

TIPO_CONTROL_ = (('T', 'Todos'),) + TIPO_CONTROL

TIPO_AUSENCIA_ = (    
    (0, 'Todas'),
    (1, 'Inculpable'),
    (11, 'Inculpable Agudos (<=30 días)'),
    (12, u'Inculpable Crónicos (>30 días)'),    
    (2, 'Accidente Denunciado'),
    (7, 'Accidente No Denunciado'),
    (3, 'Enfermedad'),
    (4, 'Familiar Enfermo'),
    (5, 'Licencias Especiales'),
    (6, 'Embarazo'),
)

TIPO_ALTA = (    
    (0, 'En Curso'),
    (1, 'Definitiva'),
    (2, u'Con Restricción'),    
)

TIPO_ACCIDENTE = (    
    (1, u'En Ocasión de Trabajo'),
    (2, u'In Itínere'),    
)

SINO = (    
    ('S', u'S'),
    ('N', u'N'),
)

ESTADO_ = (
 (0,'ACTIVOS'), 
 (1,'BAJA'),
 (2,'TODOS'), 
)

TIPO_VIGENCIA = (
 (0,'TODOS'), 
 (1,'VIGENTES'), 
 (2,'NO VIGENTES'), 
)

ESTADO_TURNO = (
 (0,'PENDIENTE'), 
 (1,'ATENDIDO'), 
 (2,'NO ASISTIÓ'), 
)

ESTADO_TURNO_ = ESTADO_TURNO + ((3,'TODOS'),)

CATEG_FISCAL = (
(1, 'IVA Responsable Inscripto'),          
(2, 'Responsable No Inscripto'),          
(3, 'IVA No Responsable'),  
(4, 'IVA Sujeto Exento'),  
(5, 'Consumidor Final'),  
(6, 'Monotributista'),  
(7, 'No Categorizado'),
(8, 'Proveedor Exterior'),  
(9, 'Consumidor Exterior'),  
(10,'IVA Liberado-Ley19.640'),  
(11,u'IVA RI – Ag. Percepción'),  
(12,'Eventual'),  
(13,'Monotributista Social'),  
(14,'Eventual Social'),  
)

TIPO_DOC = (    
(80,'CUIT'),
(86,'CUIL'),
(87,'CDI'),
(89,'LE'),
(90,'LC'),
(91,'CI Extr.'),
(92,'En trámite'),
(93,'Acta Nac.'),
(94,'Pasaporte'),
(95,'CI'),
(96,'DNI'),
(99,'CF'),
(30,'C.Migr.'),
(88,'Usado Anses'),
)

  
PROVINCIAS = (
(0,u'CABA'),
(1,'Buenos Aires'),
(2,'Catamarca'),
(3,u'Córdoba'),
(4,'Corrientes'),
(5,u'Entre Ríos'),
(6,'Jujuy'),
(7,'Mendoza'),
(8,'La Rioja'),
(9,'Salta'),
(10,'San Juan'),
(11,'San Luis'),
(12,'Santa Fe'),
(13,'Santiago del Estero'),
(14,u'Tucumán'),
(16,'Chaco'),
(17,'Chubut'),
(18,'Formosa'),
(19,'Misiones'),
(20,u'Neuquén'),
(21,'La Pampa'),
(22,'Río Negro'),
(23,'Santa Cruz'),
(24,u'Tierra del Fuego/Antártida/Islas Malvinas'),
)   


URL_API = "http://afip.grupoguadalupe.com.ar/?cuit="
EMAIL_CONTACTO = 'contacto@ironweb.com.ar'

from django.forms import Widget
from django.utils.safestring import mark_safe
class PrependWidget(Widget):
    def __init__(self, base_widget, data, *args, **kwargs):
        u"""Initialise widget and get base instance"""
        super(PrependWidget, self).__init__(*args, **kwargs)
        self.base_widget = base_widget(*args, **kwargs)
        self.data = data

    def render(self, name, value, attrs=None):
        u"""Render base widget and add bootstrap spans"""
        field = self.base_widget.render(name, value, attrs)
        return mark_safe((
            u'<div class="input-group">'
            u'    <span class="input-group-addon">%(data)s</span>%(field)s'
            u'</div>'
        ) % {'field': field, 'data': self.data})

class PostPendWidget(Widget):
    def __init__(self, base_widget, data,tooltip, *args, **kwargs):
        u"""Initialise widget and get base instance"""
        super(PostPendWidget, self).__init__(*args, **kwargs)
        self.base_widget = base_widget(*args, **kwargs)
        self.data = data
        self.tooltip = tooltip

    def render(self, name, value, attrs=None):
        field = self.base_widget.render(name, value, attrs)
        return mark_safe((
            u'<div class="input-group">'
            u'    %(field)s<span class="input-group-addon" title="%(tooltip)s">%(data)s</span>'
            u'</div>'
        ) % {'field': field, 'data': self.data,'tooltip':self.tooltip})

class PostPendWidgetBuscar(Widget):
    def __init__(self, base_widget, data,tooltip, *args, **kwargs):
        u"""Initialise widget and get base instance"""
        super(PostPendWidgetBuscar, self).__init__(*args, **kwargs)
        self.base_widget = base_widget(*args, **kwargs)
        self.data = data
        self.tooltip = tooltip

    def render(self, name, value, attrs=None):
        field = self.base_widget.render(name, value, attrs)
        return mark_safe((
            u'<div class="input-group">'
            u'    %(field)s<span class="input-group-addon btnBuscar" type="button" id="Buscar" title="%(tooltip)s"><strong>%(data)s</strong></span>'
            u''
            u'</div>'
        ) % {'field': field, 'data': self.data,'tooltip':self.tooltip})   





def inicioMes():
    hoy=date.today()
    hoy = date(hoy.year,hoy.month,1)
    return hoy

def inicioAnio():
    hoy=date.today()
    hoy = date(hoy.year,1,1)
    return hoy

def hoy():
    return date.today()    

def inicioMesAnt():
    hoy=inicioMes()
    dia =hoy - timedelta(days=30)
    return dia

def ultimoMes():
    hoy=date.today()
    dia =hoy - timedelta(days=30)
    return dia

def finMes():
    hoy=date.today()
    hoy = date(hoy.year,hoy.month,calendar.monthrange(hoy.year, hoy.month)[1])
    return hoy

def ultimo_semestre():
    hoy = date.today()
    fecha = hoy - timedelta(days=180)
    return fecha

def ultimo_anio():
    hoy = date.today()
    fecha = hoy - timedelta(days=365)
    return fecha

def proximo_anio():
    hoy = date.today()
    fecha = hoy + timedelta(days=365)
    return fecha    

import re

def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False        

def ultimoNroId(tabla):
    try:
        ultimo = tabla.objects.latest('id').id
    except:
        ultimo = 0
    return ultimo


def validar_cuit(cuit):
    # validaciones minimas    
    if len(cuit) < 11:
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    cuit = cuit.replace("-", "") # remuevo las barras

    # calculo el digito verificador:
    aux = 0
    for i in xrange(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])        


def usuario_actual(request):    
    return request.user.userprofile.id_usuario

def esAdmin(request):    
    return (request.user.userprofile.id_usuario.tipoUsr == 0)     

from entidades.models import ent_empresa
def empresa_actual(request):    
    empresa = None
    try:                    
        if 'empresa' in request.session:
            empresa = ent_empresa.objects.get(pk=int(request.session['empresa']))
    except:
        pass
    return empresa

def empresa_y_sucursales(id_empresa):
    return list(set([int(id_empresa)] + list(ent_empresa.objects.filter(casa_central__id=id_empresa, baja=False).values_list('id', flat=True))))

#Incluye la empresa del usuario + la empresa 1 universal
def empresas_habilitadas(request):    
    usu = usuario_actual(request)
    #Si es Admin puedo ver todas las empresas
    if usu.tipoUsr == 0:
        lista = list(ent_empresa.objects.filter(baja=False).values_list('id', flat=True))    
    else:
        #Sólo trae las empresas y sucursales permitidas al usuario
        # lista = empresa_y_sucursales(e.id)
        lista = usu.empresas.values_list('id', flat=True).distinct()
    return lista

import json
from decimal import Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

from django.db.models import Func, IntegerField

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = IntegerField()

class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = IntegerField()        

MESES = (
    ('1', 'Ene'),
    ('2', 'Feb'),
    ('3', 'Mar'),
    ('4', 'Abr'),
    ('5', 'May'),
    ('6', 'Jun'),
    ('7', 'Jul'),
    ('8', 'Ago'),
    ('9', 'Sep'),
    ('10','Oct'),
    ('11','Nov'),
    ('12','Dic'),
)

PERIODOS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)    

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)    

def popover_html(label, content, placement="top"):
    return label + ' &nbsp;<i class="fa fa-question-circle" data-toggle="tooltip" data-placement=placement title="'+ content +'"></i>'


def agregar_nuevo_html(label, id, title, url, callback, hint, icon):
    return label + '<a id="%s" href="%s" data-modal-head="%s" '\
    'class="agregarDatos modal-create" type="button" data-toggle="tooltip" data-modal-callback="%s" '\
    'data-placement="top" title="%s"><i class="%s"></i></a>'%(id,url,title,callback,hint,icon)
    
