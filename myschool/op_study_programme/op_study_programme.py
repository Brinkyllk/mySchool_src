from openerp.osv import fields
from openerp.osv import osv
from openerp import api


class op_study_programme(osv.Model):

    #--Code change to upper case---
    @api.onchange('code')
    def onchange_case(self, cr, uid, ids, code):
        if code != False:
            result = {'value': {
                'code': str(code).upper()
            }
            }
            return result
        else:
            return True

    _name = 'op.study.programme'
    _rec_name = 'name'
    _columns = {
        'code': fields.char('Code', required=True, size=20),
        'name': fields.char('Name',required=True, size=100),
        'res_person': fields.many2one('res.partner', 'Responsible Person'),
        'parent': fields.many2one('op.study.programme', 'Parent'),
    }