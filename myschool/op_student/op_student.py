from openerp.osv import fields, osv
import time
from openerp.tools.translate import _


class op_student(osv.Model):
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
        # 'standard_id': fields.many2one('op.standard', string='Standard', readonly=True),
        # 'course_id': fields.many2many('op.course', 'op_student_course_rel', 'student_id', 'course_id', string='Course(s)'),
        'def_batch': fields.many2one('op.batch', string='Default Batch'),
        'def_course': fields.char(string='Default Course'),
        # 'batch_ids': fields.many2many('op.batch', 'op_student_batch_rel', 'student_id', 'batch_id', string='Batch(es)'),

        'batch_ids': fields.one2many('op.student.batch.mapping', 'student_id', string='Registered Courses'),
        # 'course_ids': fields.one2many('op.student.course.mapping', 'student_id', string='Registered Courses'),

        #payment schedule
        'payment_schedule_ids': fields.one2many('op.payment.schedule', 'student_payment_id', 'Payment Schedules'),

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

        #clean NIC
        if 'id_number' in vals:
            try:
                vals['id_number'] = vals['id_number'].strip()
                if vals['id_number'] == '':
                    vals['id_number'] = None
            except:
                vals['id_number'] = None

        try:
            initials = vals['initials'].strip()
        except Exception:
            initials = ''
            pass

        if initials == '':
            full_name = vals['first_name'].strip() + ' ' + vals['last_name'].strip()
        else:
            full_name = vals['initials'] + ' ' + vals['first_name'].strip() + ' ' + vals['last_name'].strip()

        vals.update({'name': full_name})
        vals['stu_reg_number'] = self.pool.get('ir.sequence').get(cr, uid, 'myschool.op_student') or '/'
        vals.update({'is_student': True})
        stu_id = vals['stu_reg_number']

        # batchg_map_ref = self.pool.get('op.batch')
        # df_mapped_batch = batchg_map_ref.search(cr, uid, ['&', ('student_id', '=', stu_id),
        #                                                   ('default_course', '=', True)], context=context)
        # df_course = batchg_map_ref.browse(cr, uid, df_mapped_batch[0], context=context)
        # self.write(cr, uid, stu_id, {
        #     'course_id': df_course.course_id.id,
        #     'division_id': df_course.division_id.id,
        #     'batch_id': df_course.batch_id.id,
        #     'standard_id': df_course.standard_id.id,
        # }, context=context)

        return super(op_student, self).create(cr, uid, vals, context=context)

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

        return super(op_student, self).write(cr, uid, ids, values, context=context)

    def my_test(self,cr, uid, ids, context=None):
        res = {}
        reads = self.read(cr, uid, ids, fields=None, context=context)
        dictionary_reads = reads[0]
        payment_schedule_ids = dictionary_reads.get('payment_schedule_ids')
        res = payment_schedule_ids,

        return {
            'res_model': 'op.payment.schedule',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'op.payment.schedule',
            'type': 'ir.actions.act_window',
            'context': {'test': res}
                }







