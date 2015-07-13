from openerp.osv import osv, fields
import re
from openerp import api

class op_course(osv.Model):

    _name = 'op.course'
    _rec_name = 'course_code'

    _columns = {
        'course_code': fields.char(string='Code', readonly=True),
        'batch_code': fields.many2one('op.batch', string='Batch', required=True),
        'subject_code': fields.many2one('op.subject', string='Subject', required=True),
        'price':fields.float(string='Price')
    }
    _sql_constraints = [('course_code', 'UNIQUE (course_code)', 'The CODE of the COURSE must be unique!')]



    #.. Override the create method to generate the course code..#
    def create(self, cr, uid, vals, context=None):
        batch = self.pool.get('op.batch').browse(cr, uid, vals['batch_code'])
        subject = self.pool.get('op.subject').browse(cr, uid, vals['subject_code'])
        batch_code = batch.batch_code
        subject_code = subject.code

        course_code = batch_code + ' ' + subject_code
        vals.update({'course_code':course_code})

        res = super(op_course, self).create(cr, uid, vals, context=context)
        return res

    #.. Override the write method to generate the course code ..#
    def write(self, cr, uid, ids, vals, context=None):
        course_obj = self.browse(cr, uid, ids, context=context)

        #.. if subject and batch modified..#
        if ('subject_code' in vals) and ('batch_code' in vals):
            batch = self.pool.get('op.batch').browse(cr, uid, vals['batch_code'])
            batch_code = batch.batch_code
            subject = self.pool.get('op.subject').browse(cr, uid, vals['subject_code'])
            subject_code = subject.code
            course_code = batch_code + ' ' + subject_code
            vals.update({'course_code':course_code})

        #..if batch modified..#
        elif ('batch_code' in vals):
            batch = self.pool.get('op.batch').browse(cr, uid, vals['batch_code'])
            batch_code = batch.batch_code
            subject_id = course_obj.subject_code
            subject = self.pool.get('op.subject').browse(cr, uid, subject_id.id)
            subject_code = subject.code
            course_code = batch_code + ' ' + subject_code
            vals.update({'course_code': course_code})

        #..if subject modified..#
        elif ('subject_code' in vals):
            subject = self.pool.get('op.subject').browse(cr, uid, vals['subject_code'])
            subject_code = subject.code
            batch_id = course_obj.batch_code
            batch = self.pool.get('op.batch').browse(cr, uid, batch_id.id)
            batch_code = batch.batch_code
            course_code = batch_code + ' ' + subject_code
            vals.update({'course_code':course_code})
        

        res = super(op_course, self).write(cr, uid, ids,  vals, context=context)
        return res









    # #.... check passing nul values..#
    # def _check_invalid_data(self, cr, uid, ids, context=None):
    #     obj = self.browse(cr, uid, ids, context=context)
    #     new_name = str(obj.name)
    #     new_code = str(obj.code)
    #     name = new_name.replace(" ", "")
    #     code = new_code.replace(" ", "")
    #     n_name = ''.join([i for i in name if not i.isdigit()])
    #     n_code = ''.join([i for i in code if not i.isdigit()])
    #     #isalpha python inbuilt function Returns true if string
    #         #has at least 1 character and all characters are alphabetic and false otherwise.
    #     if name or code:
    #         if n_code.isalpha() or code.isdigit():
    #             if n_name.isalpha() or name.isdigit():
    #                 return True
    #     else:
    #         return False
    #
    # _constraints = [
    #                 (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
    # ]
    #
    #
    #
    # def create(self, cr, uid, vals, context=None):
    #     vals.update({'saved': True})
    #     #Reffer producy
    #     productRef = self.pool.get('product.product')
    #     product = {'name': vals['name'], 'list_price': vals['price']}
    #     pid = productRef.create(cr, uid, product, context=context)
    #     code = vals['code'].strip()
    #     name = vals['name'].strip()
    #     vals.update({'product_id': pid,'name':name, 'code':code})
    #     return super(op_course, self).create(cr, uid, vals, context=context)
    #
    #     price = re.sub('[.]', '', vals['price'])
    #     newPrice = price.isdigit()
    #     if newPrice is True:
    #         productRef = self.pool.get('product.product')
    #         product = {'name': vals['name'], 'list_price': vals['price']}
    #         pid = productRef.create(cr, uid, product, context=context)
    #         vals.update({'product_id': pid})
    #         return super(op_course, self).create(cr, uid, vals, context=context)
    #     else:
    #         raise osv.except_osv('Invalid Product Price', 'Please enter a valid price')
    #
    # def write(self, cr, uid, ids, values, context=None):
    #     if 'code' in values:
    #         code = values['code'].strip()
    #         values.update({'code': code})
    #         return super(op_course, self).write(cr, uid, ids, values, context=context)
    #
    #     #Write Product
    #     if 'name' in values:
    #         prodid = self.browse(cr, uid, ids, context=context)[0].product_id.id
    #         productRef = self.pool.get('product.product')
    #         name = values['name'].strip()
    #         values.update({'name': name})
    #         productRef.write(cr, uid, prodid, {'name': values['name']}, context=context)
    #         return super(op_course, self).write(cr, uid, ids, values, context=context)
    #
    #     if 'price' in values:
    #     #     price = re.sub('[.]', '', values['price'])
    #     #     newPrice = price.isdigit()
    #     #     if newPrice is True:
    #     #         prodid = self.browse(cr, uid, ids, context=context)[0].product_id.id
    #     #         productRef = self.pool.get('product.template')
    #     #         productRef.write(cr, uid, prodid, {'list_price': values['price']}, context=context)
    #          return super(op_course, self).write(cr, uid, ids, values, context=context)
    #     #     else:
    #     #         raise osv.except_osv('Invalid Product Price', 'Please enter a valid price')
    #
    #     if 'level' in values:
    #         return super(op_course, self).write(cr, uid, ids, values, context=context)
    #
    #
    #

