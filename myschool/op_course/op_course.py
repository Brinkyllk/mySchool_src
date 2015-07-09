from openerp.osv import osv, fields
import re
from openerp import api
# from tools.translate import _


class op_course(osv.Model):

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

    _name = 'op.course'
    # to do (Related Field)

    _columns = {
        'code': fields.char(size=8, string='Code', select=True, required=True),
        'name': fields.char(string='Name', required=True, size=74),
        'level': fields.selection([('certification', 'Certification'), ('diploma', 'Diploma'), ('degree', 'Degree')],
                                  string='Course Level'),
        'product_id': fields.many2one('product.product', 'Product', ondelete='restrict', readonly=True),
        'price': fields.related('product_id', 'list_price', string='Price', type='float'),
        'subject_ids': fields.one2many('op.subject', 'name', string='Subject(s)', options="{'create_edit': False}",
                                       readonly=True),
        # 'standard_id': fields.one2many('op.standard', 'course_id', string='Standard(s)',
        #                                options="{'create_edit': False}", readonly=True),
        'saved': fields.boolean('Saved', readonly=True),


        # ----------- test ----------
        # 'course_id': fields.many2one('op.standard', 'Course'),
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

    _constraints = [
                    (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
    ]

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the COURSE must be unique!')]

    def create(self, cr, uid, vals, context=None):
        vals.update({'saved': True})
        #Reffer producy
        productRef = self.pool.get('product.product')
        product = {'name': vals['name'], 'list_price': vals['price']}
        pid = productRef.create(cr, uid, product, context=context)
        code = vals['code'].strip()
        name = vals['name'].strip()
        vals.update({'product_id': pid,'name':name, 'code':code})
        return super(op_course, self).create(cr, uid, vals, context=context)

        price = re.sub('[.]', '', vals['price'])
        newPrice = price.isdigit()
        if newPrice is True:
            productRef = self.pool.get('product.product')
            product = {'name': vals['name'], 'list_price': vals['price']}
            pid = productRef.create(cr, uid, product, context=context)
            vals.update({'product_id': pid})
            return super(op_course, self).create(cr, uid, vals, context=context)
        else:
            raise osv.except_osv('Invalid Product Price', 'Please enter a valid price')

    def write(self, cr, uid, ids, values, context=None):
        if 'code' in values:
            code = values['code'].strip()
            values.update({'code': code})
            return super(op_course, self).write(cr, uid, ids, values, context=context)

        #Write Product
        if 'name' in values:
            prodid = self.browse(cr, uid, ids, context=context)[0].product_id.id
            productRef = self.pool.get('product.product')
            name = values['name'].strip()
            values.update({'name': name})
            productRef.write(cr, uid, prodid, {'name': values['name']}, context=context)
            return super(op_course, self).write(cr, uid, ids, values, context=context)

        if 'price' in values:
        #     price = re.sub('[.]', '', values['price'])
        #     newPrice = price.isdigit()
        #     if newPrice is True:
        #         prodid = self.browse(cr, uid, ids, context=context)[0].product_id.id
        #         productRef = self.pool.get('product.template')
        #         productRef.write(cr, uid, prodid, {'list_price': values['price']}, context=context)
             return super(op_course, self).write(cr, uid, ids, values, context=context)
        #     else:
        #         raise osv.except_osv('Invalid Product Price', 'Please enter a valid price')

        if 'level' in values:
            return super(op_course, self).write(cr, uid, ids, values, context=context)




