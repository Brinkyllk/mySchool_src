from openerp.osv import osv, fields


class op_student_batch_mapping(osv.Model):
    _name = 'op.student.batch.mapping'

    _columns = {
        'student_id': fields.many2one('op.student', string='Student'),
        'course_id': fields.many2one('op.course', 'Course', required=True),
        'batch_id': fields.many2one('op.batch', string='Batch', domain="[('course_id', '=', course_id)]",
                                    required=True, options="{'create_edit': False }"),
        'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
                                        required=True, options="{'create_edit': False }"),
        'subject_id': fields.many2many('op.subject', domain="[('standard_id', '=', standard_id)]",
                                       string='Subjects'),
        'default_course': fields.boolean('Default Course'),
        # 'product_id': fields.related('product_id', 'name', string='Related Product', type='char', readonly=True),

    }

    def create(self, cr, uid, vals, context=None):
        def_count = self.search(cr, uid,
                                ['&', ('student_id', '=', vals['student_id']), ('default_course', '=', True)],
                                context=context)
        if len(def_count) < 1:
            vals.update({'default_course': True})
        elif 'default_course' in vals:
            if vals['default_course']:
                old_def = self.browse(cr, uid, def_count, context=context)
                self.write(cr, uid, old_def[0].id, {'default_course': False}, context=context)

        return super(op_student_batch_mapping, self).create(cr, uid, vals, context=context)

    def clear_defaults(self, cr, uid, sid, context=None):
        def_count = self.search(cr, uid,
                                ['&', ('student_id', '=', sid), ('default_course', '=', True)],
                                context=context)
        if len(def_count) > 0:
            old_def = self.browse(cr, uid, def_count, context=context)
            for crs in old_def:
                self.write(cr, uid, crs.id, {'default_course': False}, context=context)

    def student_default(self, cr, uid, sid, context=None):
        def_count = self.search(cr, uid,
                                ['&', ('student_id', '=', sid), ('default_course', '=', True)],
                                context=context)
        if len(def_count) > 0:
            old_def = self.browse(cr, uid, def_count, context=context)
            return old_def[0]
        return False

    def set_default_course(self, cr, uid, sid, cid, context=None):

        def_new = self.search(cr, uid,
                              ['&', ('student_id', '=', sid), ('course_id', '=', cid)],
                              context=context)

        old_def = self.browse(cr, uid, def_new, context=context)
        if old_def:
            # self.clear_defaults(cr, uid, sid, context)
            self.write(cr, uid, old_def[0].id, {'default_course': True}, context=context)
        else:
            raise osv.except_osv(_(u'Error'), _(u'Record not found'))

        return True

    def view_details(self, cr, uid, ids, context=None):
        return {
            'res_model': 'op.payment.schedule',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'op.payment.schedule',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

    #Show data of the relevant student
    def view_schedule_line(self, cr, uid, ids, context=None):
        batchRef = self.pool.get('op.student.batch.mapping')
        batchId = batchRef.browse(cr,uid, ids, context=context)[0]
        courseId = batchRef.browse(cr,uid, batchId.course_id.id, context=context)[0]
        studentId = batchRef.browse(cr,uid, batchId.student_id.id, context=context)[0].id

        courseRef = self.pool.get('op.course')
        productId = courseRef.browse(cr,uid, courseId.id, context=context)[0]
        course_id = courseRef.browse(cr,uid, productId.product_id.id, context=context)[0]

        paymentScheduleRef = self.pool.get('op.payment.schedule')
        scheduleId = paymentScheduleRef.browse(cr,uid, course_id.id, context=context)[0].id
        paymentScheduleId = paymentScheduleRef.search(cr,uid, ['&',('product_id', '=', scheduleId), ('student_id', '=', studentId)])
        domain = [('schedule_id', '=', paymentScheduleId)]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment Schedule',
            'view_mode': 'tree',
            'view_type': 'form,tree',
            'res_model': 'op.payment.schedule.line',
            'target': 'new',
            'domain': domain
        }
