from openerp.osv import osv, fields


class op_enrollment(osv.Model):
    _name = 'op.enrollment'
    _columns = {
        'student_id': fields.many2one('op.student', string="Student Name", readonly=True),
        'batch_code': fields.many2one('op.batch', string="Batch"),
        'lead_id': fields.many2one('crm.lead', string="Lead No"),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms'),
        'template_price': fields.many2one('op.batch', 'Template Price'),
        'price': fields.float(string='Price'),
        }

    #load the specific student of the selected customer
    def default_get(self, cr, uid, fields, context=None):
        data = super(op_enrollment, self).default_get(cr, uid, fields, context=context)
        activeId = context.get('active_id')
        if activeId:
            crmRef = self.pool.get('crm.lead')
            studentRef = self.pool.get('op.student')

            crmId = crmRef.browse(cr, uid, activeId, context=context)
            partnerId = crmRef.browse(cr, uid, crmId.partner_id, context=context)
            id = partnerId.id.id
            studentId = studentRef.search(cr,uid, [('partner_id', '=', id)])[0]

            data['student_id'] = studentId
        return data
