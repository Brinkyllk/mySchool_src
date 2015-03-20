from openerp.osv import osv, fields


class op_student_batch_mapping(osv.Model):
    _name = 'op.student.batch.mapping'

    # def _sel_func(self, cr, uid, context=None):
    #     obj = self.pool.get('op.batch')
    #     ids = obj.search(cr, uid, [])
    #     res = obj.read(cr, uid, ids, ['name', 'course_id'], context)
    #     res = [(r['id'], r['name']) for r in res ]
    #     return res

    _columns = {
        'student_id': fields.many2one('op.student', string='Student'),
        'batch_id': fields.many2one('op.batch', string='Batch', domain="[('course_id', '=', course_id)]",
                                    required=True, options="{'create_edit': False }"),
        'default_course': fields.boolean('Default Course'),
        'course_id': fields.many2one('op.course', 'Course', required=True),
        # 'batch_id': fields.selection(_sel_func, string='Batch'),
    }




