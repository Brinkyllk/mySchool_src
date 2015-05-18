from openerp.osv import osv, fields


class op_subject_mapping(osv.Model):
    _name = 'op.subject.mapping'

    _columns = {
        'stu_course_map_id': fields.many2one('op.student.batch.mapping', string='Course Mapping'),
        'student_id': fields.many2one('op.student', string='Student'),
        'course_id': fields.related('course_id', string='Course'),
        'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
                                       required=True, options="{'create_edit': False }"),
        'subject_id': fields.many2one('op.subject', 'Subjects', domain="[('course_id', '=', course_id)]",
                                      required=True, options="{'create_edit': False }"),
        'grade': fields.selection([('1', 'A'), ('2', 'B'), ('3', 'C'),
                                   ('4', 'D'), ('5', 'S'), ('6', 'F'),
                                   ('7', 'Pass'), ('8', 'Fail'), ('9', 'I')
                                  ], 'Grade', required=True),

    }

    def load_course(self, cr, uid, vals, context=None):
        
        return

    def get_subjects(self, cr, uid, ids, context=None):
        return