from openerp.osv import osv, fields
from openerp.tools.translate import _


class op_student_batch_mapping(osv.Model):
    _name = 'op.student.batch.mapping'
    # _rec_name = 'subject_id'
    _columns = {
        'student_id': fields.many2one('op.student', string='Student'),
        'course_id': fields.many2one('op.course', 'Course', required=True),
        'batch_id': fields.many2one('op.batch', string='Batch', domain="[('course_id', '=', course_id)]",
                                    required=True, options="{'create_edit': False }"),
        # 'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
        #                                required=True, options="{'create_edit': False }"),
        # 'standard_id': fields.many2many('op.standard', domain="[('course_id', '=', course_id)]", string='Standards'),
        # 'subject_id': fields.one2many('op.subject', domain="[('standard_id', '=', standard_id)]", string='Subjects'),
        'subject_id': fields.many2many('op.subject', string='Subjects(s)'),

        # 'subject_id': fields.one2many('op.subject', 'standard_id', string='Subjects(s)',
        #                               options="{'create_edit': False}", readonly=True)

        # 'result_id': fields.many2many('op.subject', domain="[('subject_id', '=', subject_id)]", string='Pass Subjects'),
        'default_course': fields.boolean('Default Course'),
        # 'product_id': fields.related('product_id', 'name', string='Related Product', type='char', readonly=True),

        # 'result_table_lines': fields.one2many('op.result.mapping', 'gen_result_table', 'Result Table Lines', required=True),
        'result_table_lines_1': fields.one2many('op.result.mapping', 'gen_result_table', 'Result Table'),

        # 'product_id': fields.related('product_id', 'name', string='Related Product', type='char', readonly=True),
    }
    #Check same Course

    def _checkSameCourse(self, cr, uid, ids, context=None):
        browse = self.browse(cr, uid, ids, context=context)

        studentId = [browse.student_id.id]
        newstudentId = studentId[0]

        batch_id = [browse.batch_id.id]
        newBatchId = batch_id[0]

        courseId=[browse.course_id.id]
        newCourseId = courseId[0]

        # standardId=[browse.standard_id.id]
        # newStandardId = standardId[0]

        object = self.search(cr,uid, ['&',('student_id', '=', newstudentId),('course_id', '=', newCourseId),('batch_id', '=', newBatchId),])

        if len(object)>= 2:
            return False
        else:
            return True

    _constraints = [(_checkSameCourse, ("This course already assigned to the following student"),['course_id'])]

    # def core_subjects_get(self, cr, uid, fields, context=None):
    #     data = super(op_student_batch_mapping, self).default_get(cr, uid, fields, context=context)
    #     AA = ['student_id']
    #     print AA
    #     studentref = self.pool.get('op.student.batch.mapping')
    #     studentmap = studentref.browse(cr, uid, student_id, context=context)[0]
    #
    #
    #     # data['student_id'] = studentmap.student_id
    #     return data

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
        # check already created a  payment schedule
        if len(paymentScheduleId) == 0:
            raise osv.except_osv(_('No payment schedule'), _('You have not create a payment schedule for this product yet'))
        else:
            domain = [('schedule_id', '=', paymentScheduleId)]

        return {
            'name': 'Payment Schedule Line',
            'view_mode': 'tree',
            'view_type': 'tree',
            'res_model': 'op.payment.schedule.line',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': domain,
        }

class op_result_mapping(osv.Model):
    _name = 'op.result.mapping'
    _rec_name = 'gen_result_table'
    _columns = {
        'gen_result_table': fields.many2one('op.student.batch.mapping', 'Result Table'),
        # 'stu_course_map_id': fields.many2one('op.student.batch.mapping', string='Course Mapping'),
        # 'student_id': fields.many2one('op.student', string='Student'),
        # 'course_id': fields.many2one('op.student.batch.mapping', 'Course'),
        # 'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
        #                                required=True, options="{'create_edit': False }"),
        # 'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
        #                                 options="{'create_edit': False }"),
        'subject_id': fields.many2one('op.subject', string='Subjects',
                                      options="{'create_edit': False }"),
        # 'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
        #                                required=True, options="{'create_edit': False }"),
        'grade': fields.selection([('1', 'A'), ('2', 'B'), ('3', 'C'),
                                   ('4', 'D'), ('5', 'S'), ('6', 'F'),
                                   ('7', 'Pass'), ('8', 'Fail'), ('9', 'I')
                                   ], 'Grade'),
    }

    def default_get(self, cr, uid, fields, context=None):
        data = super(op_result_mapping, self).default_get(cr, uid, fields, context=context)
        global batch_map
        batch_map = context.get('active_id')
        return data

op_result_mapping()
