from openerp.osv import osv, fields

class op_payment_schedule_line(osv.Model):

    _name = 'op.payment.schedule.line'
    _columns = {
                'schedule_id': fields.many2one('op.payment.schedule', 'Payment Schedule'),
                'full_name': fields.char('Name'),
                'stu_reg_no': fields.char('Reg_No'),
                'due_date': fields.date('Due Date'),
                'amount': fields.float('Amount')
                }

