from openerp.osv import fields, osv
import time
from openerp.tools.translate import _


class op_student(osv.Model):

    def _get_def_batch(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        get_batch = self.pool.get('op.student.batch.mapping')
        read_batch = get_batch.browse(cr, uid, ids, context=context)
        results = read_batch.read(cr, uid, [0], ['batch_id'], context=context)
        print results
        # ['def_batch'] = res[results.id]
        return

    _name = 'op.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}
    _columns = {
        #------ personal details ------
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, ondelete="restrict", readonly=True),
        'initials': fields.char(size=20, string='Initials'),
        'first_name': fields.char(size=50, string='First Name', required=True, select=True),
        'middle_name': fields.char(size=50, string='Middle Name'),
        'last_name': fields.char(size=58, string='Last Name', required=True, select=True),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female')], string='Gender', required=True),
        'birth_date': fields.date(string='Birth Date', required=True),
        'nationality': fields.many2one('res.country', string='Nationality test'),
        'language': fields.many2one('res.lang', string='Mother Tongue'),
        'id_number': fields.char(size=10, string='NIC'),
        #'photo': fields.related('partner_id', 'image', string='Photo', type='binary', readonly=True),
        'email': fields.char(string='Email', size=128),
        'phone': fields.char(string='Phone Number', size=256),
        'user_id': fields.many2one('res.users', 'User'),
        'stu_reg_number': fields.char(string='Student No.', size=7, readonly=True),
        'partner': fields.related('partner_id', 'name', string='Related Customer', type='char', readonly=True),

        #------ Parent details ------
        'parent_name': fields.char(string='Parent Name', size=256),
        'contact_no': fields.char(string='Contact Number', size=256),

        #------ Course details ------
        'def_batch': fields.many2one('op.batch', string='Batch', readonly=True),
        'def_course': fields.many2one('op.course', 'Course', readonly=True),


        'batch_ids': fields.one2many('op.student.batch.mapping', 'student_id', string='Registered Courses'),
    }

    _sql_constraints = [('id_number', 'UNIQUE (id_number)', 'The NIC  of the Student  must be unique!')]



    def _check_nic(self, nic):
        pass

    def genid(self, cr, uid, ids, context=None):
        stud = self.browse(cr, uid, ids, context=context)[0]

        if not stud.stu_reg_number:
            id = self.pool.get('ir.sequence').get(cr, uid, 'myschool.op_student') or '/'
            self.write(cr, uid, ids, {'stu_reg_number': id}, context=context)

        return {}

    def create(self, cr, uid, vals, context=None):

        # Clean NIC
        if 'id_number' in vals:
            try:
                vals['id_number'] = vals['id_number'].strip()
                if vals['id_number'] == '':
                    vals['id_number'] = None
            except:
                vals['id_number'] = None
        # Fix initials if empty
        try:
            initials = vals['initials'].strip()
        except Exception:
            initials = ''
            pass

        if initials == '':
            full_name = vals['first_name'].strip() + ' ' + vals['last_name'].strip()
        else:
            full_name = vals['initials'] + ' ' + vals['first_name'].strip() + ' ' + vals['last_name'].strip()

        vals.update({'name': full_name})  # Update Partner record
        # Get student ID
        # Get student ID
        vals['stu_reg_number'] = self.pool.get('ir.sequence').get(cr, uid, 'myschool.op_student') or '/'
        vals.update({'is_student': True})  # Partner type is student
        # vals.update({'stu_reg_id': vals['stu_reg_number']})  # Support backwards compatible

        # Save student and get record id
        stu_id = super(op_student, self).create(cr, uid, vals, context=context)

        # Many to Many course logic
        course_map_ref = self.pool.get('op.student.batch.mapping')  # get reference to object
        # Validate Course mandatory
        # de_course = vals['course_id']
        course_count = course_map_ref.search(cr, uid, [('student_id', '=', stu_id)], count=True, context=context)
        if course_count < 1:
            if vals['course_id'] == 0:
                raise osv.except_osv(_(u'Error'), _(u'Course is mandatory'))
            return

        # Assign default course
        def_course_id = course_map_ref.search(cr, uid,
                                              ['&', ('student_id', '=', stu_id),
                                               ('default_course', '=', True)],
                                              context=context)
        def_course = course_map_ref.browse(cr, uid, def_course_id, context=context)

        # vals.update({'course_id': def_course[0].course_id.id})
        self.write(cr, uid, [stu_id], {'def_course': def_course[0].course_id.id,
                                       'def_batch': def_course[0].batch_id.id, }, context=context)
        return stu_id

    def write(self, cr, uid, ids, values, context=None):

        #clean NIC
        if 'id_number' in values:
            values['id_number'] = values['id_number'].strip()

        exstu = self.browse(cr, uid, ids, context=context)[0]
        # Rename the partner name
        initials = '' if not exstu.initials else exstu.initials
        first_nm = '' if not exstu.first_name else exstu.first_name
        last_nm = '' if not exstu.last_name else exstu.last_name

        #IF initials are change
        if 'initials' in values:
            initials = values['initials'].strip()

        #IF first_name are change
        if 'first_name' in values:
            first_nm = values['first_name'].strip()

        #IF first_name are change
        if 'last_name' in values:
            last_nm = values['last_name'].strip()

        full_name = initials + '  ' + first_nm + ' ' + last_nm
        values.update({'name': full_name})

        if 'batch_ids' in values:
            # Many to Many course logic
            course_map_ref = self.pool.get('op.student.batch.mapping')  # get reference to object
            # Validate Course mandatory
            course_count = course_map_ref.search(cr, uid, [('student_id', '=', ids[0])], count=True, context=context)
            if course_count < 1:
                raise osv.except_osv(_(u'Error'), _(u'Course is mandatory'))
                return False

            # Assign default course
            course_map_ref.clear_defaults(cr, uid, ids[0], context=context)
            super(op_student, self).write(cr, uid, ids, values, context=context)
            stdc = course_map_ref.student_default(cr, uid, ids[0], context=context)

            if stdc:
                super(op_student, self).write(cr, uid, ids, {'def_course': stdc.course_id.id,
                                                             'def_batch': stdc.batch_id.id, }, context=context)
                return True
            else:
                coursemaps = course_map_ref.search(cr, uid, [('student_id', '=', ids[0])], context=context)
                setmap = course_map_ref.browse(cr, uid, coursemaps[0], context=context)
                course_map_ref.write(cr, uid, setmap.id, {'default_course': True}, context=context)
                super(op_student, self).write(cr, uid, ids, {'def_course': setmap.course_id.id,
                                                             'def_batch': setmap.batch_id.id, }, context=context)
                return True

        return super(op_student, self).write(cr, uid, ids, values, context=context)



