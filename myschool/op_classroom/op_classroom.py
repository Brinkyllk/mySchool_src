from openerp.osv import osv, fields
from openerp import api


class op_classroom(osv.osv):

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

    _name = 'op.classroom'

    _columns = {
        'name': fields.char(size=16, string='Name', required=True),
        'code': fields.char(size=8, string='Code', required=True),
        # 'course_id': fields.many2one('op.course', 'Course', required=True),
        # 'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'capacity': fields.integer(size=5, string='No. Of Person'),
        # 'facility': fields.many2many('op.facility', 'classroom_facility_rel', 'op_classroom_id', 'op_facility_id',
        #                              string='Facilities'),
        'asset_line': fields.one2many('op.asset', 'asset_id', 'Asset', required=True),
    }

    #.... check passing nul values..#
    def _check_invalid_data(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        new_name = str(obj.name)
        new_code = str(obj.code)
        name = new_name.replace(" ", "")
        code = new_code.replace(" ", "")
        n_name = ''.join([i for i in name if not i.isdigit()])
        n_code = ''.join([i for i in code if not i.isdigit()])
        #isalpha python inbuilt function Returns true if string
            #has at least 1 character and all characters are alphabetic and false otherwise.
        if name or code:
            if n_code.isalpha() or code.isdigit():
                if n_name.isalpha() or name.isdigit():
                    return True
        else:
            return False

    def _check_capacity(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            no_persons = obj.capacity
            if no_persons == 0:
                return False
            else:
                return True

    _constraints = [
        (_check_capacity,'Number of Persons cannot be zero', ['capacity']),
        (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
    ]


op_classroom()


class op_asset(osv.osv):
    _name = 'op.asset'

    _columns = {
        'asset_id': fields.many2one('op.classroom', 'Asset'),
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'code': fields.char('Code', size=256),
        'product_uom_qty': fields.float('Quantity', required=True),

    }
