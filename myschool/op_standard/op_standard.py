from openerp.osv import fields
from openerp.osv import osv


class op_standard(osv.Model):
    _name = 'op.standard'
    _columns = {
        'code': fields.char(size=8, string='Code', required=True),
        'name': fields.char(size=32, string='Name', required=True),
    }
