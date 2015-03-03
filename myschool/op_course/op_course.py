from openerp.osv import osv, fields
# from tools.translate import _


class op_course(osv.Model):
    _name = 'op.course'
    _columns = {
        'name': fields.char(size=100, string='Name', required=True),
        'code': fields.char(size=8, string='Code', required=True),
        'level': fields.selection([('certification', 'Certification'), ('diploma', 'Diploma'), ('degree', 'Degree')],
                                  string='Evaluation Type'),
        # 'payment_term': fields.many2one('account.payment.term', 'Payment Term'),
        'subject_ids': fields.many2many('op.subject', 'op_course_subject_rel', 'course_id',
                                        'subject_id', string='Subject(s)'),
    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the COURSE must be unique!')]

