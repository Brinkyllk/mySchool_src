from openerp.osv import osv, fields
from openerp import api
# from tools.translate import _


class op_course(osv.Model):
    _name = 'op.course'
    # to do (Related Field)

    _columns = {
        'code': fields.char(size=8, string='Code', required=True),
        'name': fields.char(string='Name', required=True),
        'level': fields.selection([('certification', 'Certification'), ('diploma', 'Diploma'), ('degree', 'Degree')],
                                  string='Course Level'),
        'product_id': fields.many2one('product.product', 'Product', ondelete='restrict', readonly=True),
        'price': fields.related('product_id', 'list_price', string='Price', type='char'),
        # 'category': fields.related('uom_id', 'category_id', string='Category', type='char'),
        # 'subject_ids': fields.many2many('op.subject', 'op_course_subject_rel', 'course_id', 'subject_id',
        #                                 string='Subject(s)'),
        'subject_ids': fields.one2many('op.subject', 'name', string='Subject(s)', options="{'create_edit': False}", readonly=True),
        # 'standard_ids': fields.many2many('op.standard', 'op_course_standard_rel', 'course_id', 'semester_id',
        #                                  string='Standard(s)'),
        #'standard_id': fields.one2many('op.standard',  'course_id', string='Standards', options="{'create_edit': False }")
        'standard_id': fields.one2many('op.standard', 'course_id', string='Standard(s)', options="{'create_edit': False}", readonly=True)


        # ----------- test ----------
        # 'course_id': fields.many2one('op.standard', 'Course'),
    }


    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the COURSE must be unique!')]


    def create(self, cr, uid, vals, context=None):
        #Reffer producy
        productRef = self.pool.get('product.product')

        product = {'name': vals['name'], 'list_price': vals['price']}
        pid = productRef.create(cr, uid, product, context=context)
        vals.update({'product_id': pid})

        return super(op_course, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, values, context=None):
        #Write Product
        if 'name' in values:
            prodid = self.browse(cr, uid, ids, context=context)[0].product_id.id
            productRef = self.pool.get('product.product')
            productRef.write(cr, uid, prodid, {'name': values['name']}, context=context)
        return super(op_course, self).write(cr, uid, ids, values, context=context)



