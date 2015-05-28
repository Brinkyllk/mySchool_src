from openerp.osv import osv, fields
import time

class op_payment_schedule_line(osv.Model):

    _name = 'op.payment.schedule.line'
    _columns = {
                'schedule_id': fields.many2one('op.payment.schedule', 'Payment Schedule'),
                'full_name': fields.char('Student Name'),
                'stu_reg_no': fields.char('Student No'),
                'due_date': fields.date('Due Date'),
                'amount': fields.float('Amount')
                }

    def create_invoice(self, cr, uid, ids, context={}):
        """ Create invoice for fee payment process of student """
        scheduleLineRef = self.pool.get('op.payment.schedule.line')
        scheduleRef = self.pool.get('op.payment.schedule')
        studentRef = self.pool.get('op.student')

        scheduleLineId = scheduleLineRef.browse(cr, uid, ids, context=context)[0]
        scheduleId = scheduleLineRef.browse(cr, uid, scheduleLineId.schedule_id.id, context=context)[0]
        newScheduleId = scheduleId.id

        studentId = scheduleRef.read(cr, uid, newScheduleId, ['student_id'])
        newStudentId = studentId.get('student_id')[0]

        paymentTerm = scheduleRef.read(cr, uid, newScheduleId, ['payment_term'])
        newPaymentTerm = paymentTerm.get('payment_term')[0]

        partnerId = studentRef.read(cr, uid, newStudentId,['partner_id'])
        newPartnerId = partnerId.get('partner_id')[0]

        price = scheduleLineRef.read(cr, uid, newScheduleId,['amount'])['amount']

        dueDate = scheduleLineRef.browse(cr, uid, scheduleLineId.due_date, context=context)[0]
        newDueDate = dueDate.id


        invoice_pool = self.pool.get('account.invoice')

        default_fields = invoice_pool.fields_get(cr, uid, context=context)
        invoice_default = invoice_pool.default_get(cr, uid, default_fields, context=context)

        for student in self.browse(cr, uid, ids, context=context):

            onchange_partner = invoice_pool.onchange_partner_id(cr, uid, [], type='out_invoice', \
                                partner_id=newPartnerId)
            invoice_default.update(onchange_partner['value'])


            invoice_data = {
                            'partner_id': newPartnerId,
                            'date_invoice': time.strftime('%Y-%m-%d'),
                            'product_id': scheduleLineId,
                            'date_due': newDueDate,
                            'payment_term': newPaymentTerm,
                            }

        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(cr, uid, invoice_default, context=context)

        models_data = self.pool.get('ir.model.data')
        form_view = models_data.get_object_reference(cr, uid, 'account', 'invoice_form')
        tree_view = models_data.get_object_reference(cr, uid, 'account', 'invoice_tree')
        value = {
                'domain': str([('id', '=', invoice_id)]),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'view_id': False,
                'views': [(form_view and form_view[1] or False, 'form'),
                          (tree_view and tree_view[1] or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': invoice_id,
                'target': 'current',
                'nodestroy': True
            }
        return value

