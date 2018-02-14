# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

from types import *

#---CLASE CURSO---

class curso(osv.osv):

  _name = "sie.curso"
  _description = "Cursos"
  _columns = {
    'nombre':fields.char('Nombre', size=30, required=True),
    'precio':fields.char('Precio €', size=10, required=True),
    
}
  # Restriccion unica al campo NIF
  _sql_constraints = [
    ('nombre_unique', 'unique(nombre)', 'El nombre del curso debe ser unico'),
  ]
curso()

#---CLASE EDICION ---
class edicion(osv.osv):
    _name = "sie.edicion"
    _description = "Ediciones"
    
    _columns = { 
        'curso':fields.many2one('sie.curso','Curso', ondelete='cascade'), 
      #'edicion':fields.char('Edicion',size=20,required=True),
        'edicion':fields.many2one('product.template', 'Edicion', ondelete='set null'),
        'fecha_inicio':fields.date('Fecha_inicio', size=20),
        'fecha_fin':fields.date('Fecha_fin', size=64),
        'centro':fields.many2one('res.company', 'Centro',ondelete='cascade',select=True),
        'estado':fields.boolean('¿Finalizado?'),
    }

    _sql_constraints = [
        ('curso_unique', 'unique(curso,edicion)', 'Curso con edicion ya seleccionada!'),
    ]

edicion()
#---CLASE PROFESOR ---
class profesor(osv.osv):
    _name = "sie.profesor"
    _description = "Profesores"
    _columns = { 
      'nombre':fields.many2one('hr.employee', 'Profesor', ondelete='set null'),    
      'direccion':fields.char('Direccion',size=30,required=True),
      'localidad':fields.char('Localidad',size=20,required=True),
      'nif':fields.char('NIF',size=20,required=True),
      'curso':fields.many2one('product.template','Curso', ondelete='cascade', select=True),
      'edicion':fields.many2one('product.template','Edicion', ondelete='cascade', select=True),
    }

    _sql_constraints = [
       ('edicion_unique','unique(curso,edicion)', 'La edicion solo la imparte un unico profesor'),
  ]
profesor()

class alumnos(osv.osv):
    _name = "sie.alumno"
    _description = "Alumnos"
    _columns = { 
        'nombre':fields.many2one('res.partner', 'Nombre', required=True),    
        'direccion':fields.char('Direccion',size=30,required=True),
        'localidad':fields.char('Localidad',size=20,required=True),
        'nif':fields.char('NIF',size=20,required=True),
        'curso':fields.many2one('product.template','Curso', ondelete='cascade', select=True),
        'edicion':fields.many2one('product.template','Edicion', ondelete='cascade', select=True),
    }

alumnos()

class inscripcion(osv.osv):
    _name =  "sie.inscripcion"
    _description= "Inscripciones"
    _columns = {
        
       'alumnos':fields.many2one('res.partner', 'Alumnos', ondelete='no action', select=True),
       'edicion':fields.many2one('sie.edicion','Edicion', ondelete='cascade', select=True),
       'state': fields.selection([('pendiente_inscripcion', 'Pendiente Inscripcion'),
            ('inscrito', 'Inscrito'),
            ('enviarfactura', 'Factura'),          
            ('aprobado', 'Aprobado'),
            ('suspenso', 'Suspenso')
            ],
            'State', readonly=True,
            help='Estado de la inscripcion.')
    }
    _defaults = {
        'state' : lambda *a : 'pendiente_inscripcion'
    }
    #-----Metodos Estados de Transicion-----#
    def pendiente_inscripcion(self, cr, uid, ids,context=None) :
        self.write(cr, uid, ids, { 'state' : 'pendiente_inscripcion'},context=context)
        return True

    def inscrito(self, cr, uid, ids,context=None) :
        self.write(cr, uid, ids, { 'state' : 'inscrito'},context=context)
        return True

    def enviarfactura(self, cr, uid, ids,context=None) :
        self.write(cr, uid, ids, { 'state' : 'enviarfactura'},context=context)
        return True 

    def aprobado(self, cr, uid, ids,context=None) :
        self.write(cr, uid, ids, { 'state' : 'aprobado'},context=context)
        return True

    def suspenso(self, cr, uid, ids,context=None) :
        self.write(cr, uid, ids, { 'state' : 'suspenso'},context=context)
        return True  

inscripcion()
