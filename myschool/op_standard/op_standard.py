from openerp.osv import fields
from openerp.osv import osv


class op_standard(osv.Model):
    _name = 'op.standard'
    _description = 'Standard'
    _columns = {
        'code': fields.char(size=8, string='Code', required=True),
        'name': fields.char(size=32, string='Name', required=True),
    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Standard must be unique!')]
