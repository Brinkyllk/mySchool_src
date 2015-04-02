from openerp.osv import osv, fields
# from tools.translate import _


class op_course(osv.Model):
    _name = 'op.course'
    _inherits = {'product.product': 'product_id'}

    _columns = {
        'code': fields.char(size=8, string='Code', required=True),
        'level': fields.selection([('certification', 'Certification'), ('diploma', 'Diploma'), ('degree', 'Degree')],
                                  string='Course Level'),
        # 'subject_ids': fields.many2many('op.subject', 'op_course_subject_rel', 'course_id',
        #                                 'subject_id', string='Subject(s)'),
        'product_id': fields.many2one('product.product', 'Product', select=True, ondelete='restrict', readonly=True),
        'product': fields.related('product_id', 'name', string='Course', type='char', readonly=True),
        'subject_ids': fields.many2many('op.subject', 'op_course_subject_rel', 'course_id', 'subject_id',
                                        string='Subjects'),


        # ----------- test ----------
        # 'course_id': fields.many2one('op.standard', 'Course'),
    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the COURSE must be unique!')]
