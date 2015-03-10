from openerp.osv import osv, fields
# from tools.translate import _


class op_course(osv.Model):
    _name = 'op.course'
    _inherits = {'product.product': 'product_id'}

    _columns = {
        'code': fields.char(size=8, string='Code', required=True),
        # 'name': fields.char(size=100, string='Name', required=True),
        'level': fields.selection([('certification', 'Certification'), ('diploma', 'Diploma'), ('degree', 'Degree')],
                                  string='Course Level'),
        # 'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
        'subject_ids': fields.many2many('op.subject', 'op_course_subject_rel', 'course_id',
                                        'subject_id', string='Subject(s)'),
        'product_id': fields.many2one('product.product', 'Product', ondelete='restrict', readonly=True),
        # 'list_price': fields.many2one('product.product', 'Product', ondelete="restrict", readonly=False),
        # 'batch_id': fields.one2many('op.batch', 'batch_id', string='Batch'),
        'product': fields.related('product_id', 'name', string='Product', type='char', readonly=True),
    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the COURSE must be unique!')]

