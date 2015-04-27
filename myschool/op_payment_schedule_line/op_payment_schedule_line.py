from openerp.osv import osv, fields

class op_payment_schedule_line(osv.Model):

    def default_get(self, cr, uid, fields_list, context=None):

        res = []
        test_list = context.__getitem__('test')
        print test_list

        payment_schedule_line_obj = self.pool.get('op.payment.schedule.line')

        for line in test_list:
            for list2 in line:
                # for element in list2:
                sub_lines = []
                sub_lines.append((0, 0, {'due_date': list2[0], 'amount': list2[1]}))
                # idea_id = payment_schedule_line_obj.create(cr, uid, {'payment_schedule_line_ids': sub_lines}, context)

        return sub_lines

    _name = 'op.payment.schedule.line'
    _columns = {
                'payment_schedule_line_ids': fields.many2one('op.payment.schedule', 'Payment Schedule'),
                'due_date': fields.date('Due Date'),
                'amount': fields.float('Amount'),
                }


