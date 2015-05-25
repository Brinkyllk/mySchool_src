from openerp.osv import fields
from openerp.osv import osv


class op_semester(osv.Model):
    _name = 'op.semester'
    _description = 'Semester'
    _columns = {
        'code': fields.char(size=8, string='Code', required=True),
        'name': fields.char(size=32, string='Name', required=True),
        # 'semester_id': fields.many2one('op.standard', 'Academic Term'),
    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Standard must be unique!')]


class op_standard(osv.Model):
    _name = 'op.standard'
    _description = 'Standard'
    _columns = {
        # 'course_ids': fields.one2many('op.course', 'course_id', string='Course'),
        'course_id': fields.many2one('op.course', 'Course', select=True, required=True),
        'semester_id': fields.many2one('op.semester', 'Academic Term', select=True, required=True),
        # 'semester_ids': fields.one2many('op.semester', 'semester_id', string='Academic Term'),
        # 'code': fields.char(size=8, string='Code', required=True),
        'name': fields.char(size=32, string='Standard', readonly=True),
        'subject_id': fields.one2many('op.subject', 'standard_id', string='Subjects(s)',
                                      options="{'create_edit': False}", readonly=True)
    }

    def create(self, cr, uid, vals, context=None):
        course = self.pool.get('op.course').browse(cr, uid, vals['course_id'])
        semester = self.pool.get('op.semester').browse(cr, uid, vals['semester_id'])
        course_code = course.code
        semester_code = semester.code

        stand = course_code + ' ' + semester_code
        vals.update({'name': stand})

        res = super(op_standard, self).create(cr, uid, vals, context=context)
        return res

    _sql_constraints = [('name', 'UNIQUE (name)', 'The Standard must be unique!')]
