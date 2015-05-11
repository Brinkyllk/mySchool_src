from openerp.osv import osv, fields


class op_student_batch_mapping(osv.Model):
    _name = 'op.student.batch.mapping'

    _columns = {
        'student_id': fields.many2one('op.student', string='Student'),
        'batch_id': fields.many2one('op.batch', string='Batch', domain="[('course_id', '=', course_id)]",
                                    required=True, options="{'create_edit': False }"),
        'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
                                        required=True, options="{'create_edit': False }"),

        'subject_id': fields.many2one('op.subject', string='Subjects', domain="[('standard_id', '=', standard_id)]",
                                       required=True),


        'default_course': fields.boolean('Default Course'),
        'course_id': fields.many2one('op.course', 'Course', required=True),
        'product_id': fields.related('product_id', 'name', string='Related Product', type='char', readonly=True),

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

