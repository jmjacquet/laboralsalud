# -*- coding: utf-8 -*-
from datetime import datetime, timedelta,date

TIPO_USR = (
    (0, u'Administrador'),
    (1, u'Médico/Profesional'),
    (2, u'Encargado'),
)

TIPO_ENTIDAD = (    
    (1, 'Cliente'),
    (2, 'Proveedor'),
    (3, 'Empleado'),
)

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
(24,'Tierra del Fuego/Antártida/Islas Malvinas'),
)   

