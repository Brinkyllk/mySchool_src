from openerp.osv import fields
from openerp.osv import osv
from openerp import api

class op_study_programme(osv.Model):
    _name = 'op.study.programme'
    _columns = {
        'code': fields.char('Code', required=True, size=20),
        'name': fields.char('Name',required=True, size=100),
        'res_person': fields.many2one('res.partner', 'Responsible Person', required=True, ondelete="restrict"),
        'parent': fields.many2one('op.study.programme', 'Parent'),
    }