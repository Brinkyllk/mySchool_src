from openerp.osv import fields
from openerp.osv import osv
from openerp import api

class op_study_programme(osv.Model):
    _name = 'op.study.programme'
    _columns = {
        'code': fields.char('Code', required=True, size=8),
        'name': fields.char('Name',required=True, size=100),
        'res_person': fields.char('Responsible Person', required=True),
        'parent': fields.char('Parent', required=True),
    }