from openerp.osv import osv, fields


class op_student_sub_mapping(osv.Model):
    _name = 'op.student.sub.mapping'
    _columns = {
        'student_id': fields.many2one('op.student', string='Student'),
        'subject_id': fields.many2one('op.course', string='Course'),
        # 'default_course': fields.boolean('Default Course'),
        # 'division_id': fields.many2one('op.division', string='Division'),
        # 'batch_id': fields.many2one('op.batch', string='Batch', required=False),
        # 'standard_id': fields.many2one('op.standard', string='Semester', required=False)
    }