from openerp.osv import fields
from openerp.osv import osv
from openerp import api


class op_semester(osv.Model):

    @api.onchange('code')
    def onchange_case(self, cr, uid, ids, code):
        if code != False:
            result = {'value': {
                'code': str(code).upper()
            }
            }
            return result
        else:
            return True

    _name = 'op.semester'
    _description = 'Semester'
    _columns = {
        'code': fields.char(size=8, string='Code', required=True),
        'name': fields.char(size=32, string='Name', required=True),
        # 'semester_id': fields.many2one('op.standard', 'Academic Term'),
    }

    #.... check passing nul values..#
    def _check_invalid_data(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        new_name = str(obj.name)
        new_code = str(obj.code)
        name = new_name.replace(" ", "")
        code = new_code.replace(" ", "")
        n_name = ''.join([i for i in name if not i.isdigit()])
        n_code = ''.join([i for i in code if not i.isdigit()])
        #isalpha python inbuilt function Returns true if string
            #has at least 1 character and all characters are alphabetic and false otherwise.
        if name or code:
            if n_code.isalpha() or code.isdigit():
                if n_name.isalpha() or name.isdigit():
                    return True
        else:
            return False
    _constraints = [
                    (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
    ]

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Standard must be unique!')]

    def create(self, cr, uid, vals, context=None):
        code = vals['code'].strip()
        name = vals['name'].strip()
        vals.update({'code':code, 'name':name})
        return super(op_semester, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids,  values, context=None):
        if 'name' in values:
            name = values['name'].strip()
            values.update({'name': name})
        if 'code' in values:
            code = values['code'].strip()
            values.update({'code': code})
        return super(op_semester, self).write(cr, uid, ids,  values, context=context)


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
