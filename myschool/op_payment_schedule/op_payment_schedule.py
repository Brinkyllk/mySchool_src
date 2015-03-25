from openerp.osv import osv, fields

class op_payment_schedule(osv.Model):
    _name = 'op.payment.schedule'
    _description = 'Payment Schedule'
    # _inherits = {'account.payment.term': 'account_payment_term_id'}
    _columns = {

        'product_id': fields.many2one('product.product', 'Product Name'),
        'list_price': fields.float('Product Price'),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms'),
        'invoice_date': fields.date(string='Invoice Date'),
        'student_payment_id': fields.many2one('op.student', 'Student'),
        # 'product': fields.related('product_id', 'name', string='Batch', type='char', readonly=True),
        'schedule_lines': fields.one2many('op.payment.schedule.lines', 'payment_schedule_lines_ids', string='Lines'),


    }



class op_payment_schedule_lines(osv.Model):

    _name = 'op.payment.schedule.lines'
    _columns = {
                'payment_schedule_lines_ids': fields.many2one('op.payment.schedule', 'Payment Schedule'),
                'due_date': fields.date('Due Date'),
                'amount': fields.float('Amount'),
                }


