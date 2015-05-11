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
        'schedule_lines': fields.one2many('op.payment.schedule.line', 'payment_schedule_line_ids', string='Lines'),
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
        dictionary_reads = self.read(cr, uid, ids, fields=None, context=context)[0]

        result_price = float(dictionary_reads.get('list_price'))
        payment_term_id = dictionary_reads.get('payment_term')[0]
        date_invoice = dictionary_reads.get('invoice_date')

        p_term_list = self.pool.get('account.payment.term').compute(cr, uid, payment_term_id, result_price, date_ref=date_invoice)
        res = p_term_list

        payment_schedule_obj = self.pool.get('op.payment.schedule')
        # payment_schedule_line_obj = self.pool.get('op.payment.schedule.line')
        for line in p_term_list:
            sub_lines = []
            sub_lines.append((0, 0, {'due_date': line[0], 'amount': line[1]}))

            # payment_schedule_obj.create(cr, uid, {'schedule_lines': sub_lines}, context)

            # pay_sch_line_id  = payment_schedule_obj.create(cr, uid, {'schedule_lines': sub_lines}, context)
            # vals_payment_schedule = self.id(cr, uid, line, pay_sch_line_id, context=context)
            # payment_schedule_line_obj.create(cr, uid, vals_payment_schedule)

            payment_data = ({'schedule_lines': sub_lines,
                                 })
            obj_payment = self.pool.get('op.payment.schedule')
            payid = obj_payment.create(cr, uid, payment_data, context=context )
            print payid
            # obj_payment.update(payid)

        return {
            'name': 'Payment Schedule Line',
            'view_mode': 'tree',
            'view_type': 'tree',
            'res_model': 'op.payment.schedule.line',
            'type': 'ir.actions.act_window',
            'context': {'test': payid}
                }
