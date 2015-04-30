from openerp.osv import osv, fields
import time

class op_payment_schedule(osv.Model):
    _name = 'op.payment.schedule'
    _description = 'Payment Schedule'
    _columns = {

        'product_id': fields.many2one('product.product', 'Product Name'),
        'list_price': fields.float('Product Price'),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms'),
        'invoice_date': fields.date(string='Invoice Date'),
        'student_id': fields.many2one('op.student', 'Student'),
        # 'product': fields.related('product_id', 'name', string='Batch', type='char', readonly=True),
        'schedule_lines': fields.one2many('op.payment.schedule.line', 'payment_schedule_line_ids', string='Lines'),
    }

    _defaults = {
        'invoice_date': time.strftime('%Y-%m-%d'),
    }

    #Pass default values to product name and product price
    def default_get(self, cr, uid,  fields, context=None):
        res = super(op_payment_schedule, self).default_get(cr, uid, fields, context=context)
        if 'product_id' in fields:
            print fields
            res['product_id'] = context.get('active_id')

            #product price
            productId=[res['product_id']]

            cr.execute('SELECT list_price FROM product_template '\
                   'WHERE id=%s',(productId))

            allPrice = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            price = allPrice[0].id
            res['list_price'] = price
        return res


    def my_test(self,cr, uid, ids, context=None):
        reads = self.read(cr, uid, ids, fields=None, context=context)
        print reads[0]
        dictionary_reads = reads[0]
        product_id = dictionary_reads.get('product_id')[0]
        result_price = float(dictionary_reads.get('list_price'))#getlistprice
        tuple_payment_term_id = dictionary_reads.get('payment_term')
        payment_term_id = tuple_payment_term_id[0]#get payment term id
        date_invoice = dictionary_reads.get('invoice_date')
        stu_id = dictionary_reads.get('student_id')
        print stu_id

        p_term_list = self.pool.get('account.payment.term').compute(cr, uid, payment_term_id, result_price, date_ref=date_invoice)

        res = p_term_list

        payment_schedule_obj = self.pool.get('op.payment.schedule')
        # payment_schedule_line_obj = self.pool.get('op.payment.schedule.line')


        for line in p_term_list:
            sub_lines = []
            sub_lines.append((0, 0, {'due_date': line[0], 'amount': line[1]}))
            payment_schedule_obj.create(cr, uid, {'schedule_lines': sub_lines}, context)
            # pay_sch_line_id  = payment_schedule_obj.create(cr, uid, {'schedule_lines': sub_lines}, context)
            # vals_payment_schedule = self.id(cr, uid, line, pay_sch_line_id, context=context)
            # payment_schedule_line_obj.create(cr, uid, vals_payment_schedule)


        return {
            'name': 'Payment Schedule Line',
            'view_mode': 'tree',
            'view_type': 'tree',
            'res_model': 'op.payment.schedule.line',
            'type': 'ir.actions.act_window',
            'context': {'test': res}
                }
