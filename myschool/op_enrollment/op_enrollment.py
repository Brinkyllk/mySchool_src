from openerp.osv import osv, fields


class op_enrollment(osv.Model):
    _name = 'op.enrollment'
    _columns = {
        'student_id': fields.many2one('op.student', string="Student Name"),
        'batch_code': fields.many2one('op.batch', string="Batch"),
        'lead_id': fields.many2one('crm.lead', string="Lead No"),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms'),
        'template_price': fields.many2one('op.batch', 'Template Price'),
        'price': fields.float(string='Price'),
        }
