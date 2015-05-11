from openerp.osv import osv, fields
import time

class op_payment_schedule(osv.Model):
    _name = 'op.payment.schedule'
    _description = 'Payment Schedule'
    _columns = {

        'product_id': fields.many2one('product.product', 'Product Name', readonly=True),
        'list_price': fields.related('product_id', 'lst_price', type='float', string='Price', readonly=True, store=True),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms', required=True),
        'invoice_date': fields.date(string='Invoice Date', required=True),
        'student_id': fields.many2one('op.student', 'Student', readonly=True),
        'line_ids': fields.one2many('op.payment.schedule.line', 'schedule_id', string='Lines'),

    }

    _defaults = {
       'invoice_date': time.strftime('%Y-%m-%d')
    }


    def default_get(self, cr, uid, fields, context=None):

        data = super(op_payment_schedule, self).default_get(cr, uid, fields, context=context)

        batchmapId = context.get('active_id')

        batchRef = self.pool.get('op.student.batch.mapping')
        courseRef = self.pool.get('op.course')
        productRef = self.pool.get('product.product')

        batchMap = batchRef.browse(cr,uid, batchmapId, context=context)[0]
        course = courseRef.browse(cr,uid, batchMap.course_id.id, context=context)[0]
        product = productRef.browse(cr, uid, course.product_id.id, context=context)[0]

        data['product_id'] = product.id
        data['list_price'] = product.lst_price
        data['student_id'] = batchMap.student_id.id

        return data


    def generate_schedule_lines(self,cr, uid, ids, context=None):
        ps_obj = self.browse(cr, uid, ids, context=context)

        result_price = ps_obj.list_price
        payment_term_id = ps_obj.payment_term.ids[0]
        date_invoice = ps_obj.invoice_date

        p_term_list = self.pool.get('account.payment.term').compute(cr, uid, payment_term_id, result_price, date_ref=date_invoice)

        payment_schedule_obj = self.pool.get('op.payment.schedule')
        for line in p_term_list:
            sub_lines = []
            sub_lines.append((0, 0, {'due_date': line[0], 'amount': line[1]}))
            payment_schedule_obj.write(cr, uid, ids, {'line_ids': sub_lines}, context=context)

        return {
            'name': 'Payment Schedule Line',
            'view_mode': 'tree',
            'view_type': 'tree',
            'res_model': 'op.payment.schedule.line',
            'type': 'ir.actions.act_window',
                }
