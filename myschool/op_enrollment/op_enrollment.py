from openerp.osv import osv, fields


class op_enrollment(osv.Model):

        #load the specific student of the selected customer
    # def default_get(self, cr, uid, fields, context=None):
    #     # reg_ref = self.browse(cr, uid, ids, )
    #     data = super(op_enrollment, self).default_get(cr, uid, fields, context=context)
    #     registration_id = context.get('active_id', False)
    #     if registration_id:
    #         crmRef = self.pool.get('crm.lead')
    #         studentRef = self.pool.get('op.student')
    #
    #         crmId = crmRef.browse(cr, uid, registration_id, context=context)
    #         partnerId = crmRef.browse(cr, uid, crmId.partner_id, context=context)
    #         id = partnerId.id.id
    #         studentId = studentRef.search(cr, uid, [('partner_id', '=', id)])[0]
    #
    #         data['student_id'] = studentId
    #     return data

    _name = 'op.enrollment'
    _columns = {
        'student_id': fields.many2one('op.student', string="Student Name", readonly=True, invisible=True),
        'batch_code': fields.many2one('op.batch', string="Batch", required=True),
        'lead_id': fields.many2one('crm.lead', string="Lead No"),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms'),
        'template_price': fields.many2one('op.batch', 'Template Price'),
        'price': fields.float(string='Price', digits=(0, 2)),
        'confirm': fields.boolean(string='Confirmed'),
        'reg_id': fields.many2one('op.registration', invisible=True, string="Registration ID")
        }

    #Check same course enrollment
    def _checkSameCourse(self, cr, uid, ids, context=None):
        browse = self.browse(cr, uid, ids, context=context)

        studentId = [browse.student_id.id]
        newstudentId = studentId[0]

        batch_id = [browse.batch_code.id]
        newBatchId = batch_id[0]

        # leadId=[browse.lead_id.id]
        # newLeadId = leadId[0]

        regId=[browse.reg_id.id]
        newRegId = regId[0]

        if newstudentId:
            object = self.search(cr, uid, ['&', ('batch_code', '=', newBatchId), ('student_id', '=', newstudentId)])
            if len(object)>= 2:
                return False
            else:
                return True

        if newRegId:
            object = self.search(cr, uid, ['&', ('batch_code', '=', newBatchId), ('reg_id', '=', newRegId)])
            if len(object)>= 2:
                return False
            else:
                return True

    # _constraints = [(_checkSameCourse, ("Course enrollments are duplicated"),['batch_code'])]

    def create(self, cr, uid, vals, context=None):
        #Minus values are not allowed for the price
        if 'price' in vals:
            price = vals['price']
            if price >= 0:
                pass
            else:
                raise osv.except_osv('Value Error', 'Minus values are not allowed for the Price')

        return super(op_enrollment, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids,  values, context=None):
        #Minus values are not allowed for the price
        if 'price' in values:
            price = values['price']
            if price >= 0:
                pass
            else:
                raise osv.except_osv('Value Error', 'Minus values are not allowed for the Price')

        ss = self.pool.get('op.student')
        sa = ss.browse(cr, uid, ids, context=context).id
        print sa

        return super(op_enrollment, self).write(cr, uid, ids,  values, context=context)

