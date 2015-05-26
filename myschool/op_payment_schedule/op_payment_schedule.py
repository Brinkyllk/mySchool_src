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
       'invoice_date': fields.date.context_today
    }

    #validate same payment term
    def _checkSamePaymentTerm(self, cr, uid, ids, context=None):
        browse = self.browse(cr, uid, ids, context=context)

        productId=[browse.product_id.id]
        newProductId = productId[0]

        studentId=[browse.student_id.id]
        newStudentId = studentId[0]

        paymentScheduleId = self.search(cr,uid, ['&',('product_id', '=', newProductId), ('student_id', '=', newStudentId)])
        if len(paymentScheduleId)>1:
            return False
        else:
            return True

        # obj = self.pool.get('op.payment.schedule.line').search(cr, uid, [('schedule_id', '=', paymentScheduleId), ], order=None)
        # if obj:
        #     for record_id in obj:
        #         details = self.pool.get('op.payment.schedule.line').read(cr, uid, record_id, ['schedule_id'])
        #         scheduleId = details.get('schedule_id')
        #         newScheduleId = scheduleId[0]
        #         print type (newScheduleId)
        #         print newScheduleId
        #         if paymentScheduleId == newScheduleId:
        #             return False
        #         return True
        # else:
        #     return True

    _constraints = [(_checkSamePaymentTerm, ("For this product already create a payment schedule"),['product_id'])]

    def default_get(self, cr, uid, fields, context=None):

        data = super(op_payment_schedule, self).default_get(cr, uid, fields, context=context)

        batchmapId = context.get('active_id')

        batchRef = self.pool.get('op.student.batch.mapping')
        courseRef = self.pool.get('op.course')
        productRef = self.pool.get('product.product')

        batchMap = batchRef.browse(cr,uid, batchmapId, context=context)[0]
        course = courseRef.browse(cr,uid, batchMap.course_id.id, context=context)[0]
        product = productRef.browse(cr, uid, course.product_id.id, context=context)[0]

        productId = product.id
        studentId = batchMap.student_id.id

        paymentScheduleRef = self.pool.get('op.payment.schedule')
        paymentScheduleId = paymentScheduleRef.search(cr,uid, ['&',('product_id', '=', productId), ('student_id', '=', studentId)])
        paymentTermId = paymentScheduleRef.browse(cr, uid, paymentScheduleId, context=context)
        newPaymentTermId = paymentScheduleRef.browse(cr, uid, paymentTermId.payment_term.id, context=context)

        data['product_id'] = product.id
        data['list_price'] = product.lst_price
        data['student_id'] = batchMap.student_id.id
        # data['payment_term'] = newPaymentTermId.id

        return data


    def generate_schedule_lines(self,cr, uid, ids, context=None):
        ps_obj = self.browse(cr, uid, ids, context=context)

        result_price = ps_obj.list_price
        payment_term_id = ps_obj.payment_term.ids[0]
        date_invoice = ps_obj.invoice_date
        student = ps_obj.student_id.id

        studentRef = self.pool.get('op.student').read(cr, uid, student, ['last_name', 'first_name', 'stu_reg_number'])
        firstName = studentRef['first_name']
        lastName = studentRef['last_name']
        full_name = str(firstName + ' ' + lastName)
        studentRegNo = str(studentRef['stu_reg_number'])

        p_term_list = self.pool.get('account.payment.term').compute(cr, uid, payment_term_id, result_price, date_ref=date_invoice, )

        payment_schedule_obj = self.pool.get('op.payment.schedule')
        for line in p_term_list:
            sub_lines = []
            sub_lines.append((0, 0, {'due_date': line[0], 'amount': line[1], 'full_name':full_name, 'stu_reg_no':studentRegNo}))
            payment_schedule_obj.write(cr, uid, ids, {'line_ids': sub_lines}, context=context)
        return True