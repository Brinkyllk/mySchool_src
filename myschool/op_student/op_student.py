from openerp.osv import fields, osv
from datetime import date, datetime
from openerp.tools.translate import _
from validate_email import validate_email
import re
import time

class op_student(osv.Model):
    # def _get_def_batch(self, cr, uid, ids, field_name, arg, context=None):
    #     res = {}
    #     get_batch = self.pool.get('op.student.batch.mapping')
    #     read_batch = get_batch.browse(cr, uid, ids, context=context)
    #     results = read_batch.read(cr, uid, [0], ['batch_id'], context=context)
    #     print results
    #     # ['def_batch'] = res[results.id]
    #     return

    _name = 'op.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}
    _columns = {
        #------ personal details ------
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, ondelete="restrict", readonly=True),
        'initials': fields.char(size=20, string='Initials'),
        'first_name': fields.char(size=15, string='First Name', required=True, select=True),
        'middle_name': fields.char(size=15, string='Middle Name'),
        'last_name': fields.char(size=20, string='Last Name', required=True, select=True),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female')], string='Gender', required=True),
        'birth_date': fields.date(string='Birth Date', required=True),
        'nationality': fields.many2one('res.country', string='Nationality test'),
        'language': fields.many2one('res.lang', string='Mother Tongue'),
        'id_number': fields.char(size=10, string='NIC'),
        #'photo': fields.related('partner_id', 'image', string='Photo', type='binary', readonly=True),
        'email': fields.char(string='Email', size=128),
        'phone': fields.char(string='Phone Number', size=256),

        'address_line1': fields.char('address line1', size=20),
        'address_line2': fields.char('address line2', size=25),
        'town': fields.char('town', size=25),
        'province': fields.char('province', size=20),
        'nation': fields.char('nation', size=20),

        'user_id': fields.many2one('res.users', 'User'),
        'stu_reg_number': fields.char(string='Student No.', size=7, readonly=True),
        'partner': fields.related('partner_id', 'name', string='Related Customer', type='char', readonly=True),

        #------ Parent details ------
        'parent_name': fields.char(string='Parent Name', size=60),
        'contact_no': fields.char(string='Contact Number', size=12),

        #------ Course details ------
        'def_batch': fields.many2one('op.batch', string='Batch', readonly=True),
        'def_course': fields.many2one('op.course', 'Course', readonly=True),
        'def_standard': fields.many2one('op.standard', 'Standard', readonly=True),

        #------ Map many Courses ------
        'batch_ids': fields.one2many('op.student.batch.mapping', 'student_id', string='Registered Courses'),

        #payment schedule
        'payment_schedule_id': fields.one2many('op.payment.schedule', 'student_id', 'Payment Schedules')

    }

    _sql_constraints = [('id_number', 'UNIQUE (id_number)', 'The NIC  of the Student  must be unique!')]

    def _check_nic(self, nic):
        pass

    #------check spaces in address line one----#
    def _check_add_l_one(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.address_line1)
        if not value:
            return False
        else:
            return True

    #------check spaces in address line two----#
    def _check_add_l_two(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.address_line2)
        if not value:
            return False
        else:
            return True

    #-----check spaces in town-----------------#
    def _check_town(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.town)
        if not value:
            return False
        else:
            return True

    #-----check spaces in province--------------#
    def _check_province(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.province)
        if not value:
            return False
        else:
            return True

    #-----check spaces in country---------------#
    def _check_nation(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.nation)
        new_value = value.replace(" ", "")
        if not new_value or not new_value.isalpha():
            return False
        else:
            return True


    #.... check passing nul values..#
    def _check_invalid_data(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        fnew_name = str(obj.first_name)
        lnew_code = str(obj.last_name)
        fname = fnew_name.replace(" ", "")
        lname = lnew_code.replace(" ", "")
        #isalpha python inbuilt function Returns true if string
            #has at least 1 character and all characters are alphabetic and false otherwise.
        if fname or lname:
            if fname.isalpha() and lname.isalpha():
                return True
            else:
                return False
        else:
            return False

    # email validation........
    def validate_email(self, cr, uid, ids, email):
        if email is False:
            return True
        is_valid = validate_email(email)
        if is_valid is False:
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid email address'))
        return True

    def validate_NIC(self, cr, uid, ids, id_number):
        if id_number is None:
            return True
        if id_number is False:
            return True
        if re.match('^\d{9}(X|V)$', id_number) == None:
            raise osv.except_osv('Invalid NIC', 'Please enter a valid NIC')
        return True

    #phone number validation for student
    def phoneNumberValidation(self, cr, uid, ids, phoneNumber):
        phone_re = re.compile(ur'^(\+\d{1,1}[- ]?)?\d{10}$')
        valid_phone = False
        if phoneNumber is False:
            return True
        if phone_re.match(phoneNumber):
            valid_phone=True
            return True
        else:
            raise osv.except_osv(_('Invalid Phone Number'), _('Please enter a valid Phone Number'))

    #phone number validation for parent
    def phoneNumberValidationParent(self, cr, uid, ids, phoneNumber):
        phone_re = re.compile(ur'^(\+\d{1,1}[- ]?)?\d{10}$')
        valid_phone = False
        if phoneNumber is False:
            return True
        if phone_re.match(phoneNumber):
            valid_phone=True
            return True
        else:
            raise osv.except_osv(_('Invalid Phone Number'), _('Please enter a valid Phone Number'))

    def genid(self, cr, uid, ids, context=None):
        stud = self.browse(cr, uid, ids, context=context)[0]

        if not stud.stu_reg_number:
            id = self.pool.get('ir.sequence').get(cr, uid, 'myschool.op_student') or '/'
            self.write(cr, uid, ids, {'stu_reg_number': id}, context=context)

        return {}

    def create(self, cr, uid, vals, context=None):
        # email validation on write
        if 'email' in vals:
            self.validate_email(cr, uid, [], vals['email'])

        # phone number validation on create
        if 'phone' in vals:
            self.phoneNumberValidation(cr, uid, [], vals['phone'])
        if 'contact_no' in vals:
            self.phoneNumberValidationParent(cr, uid, [], vals['contact_no'])

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

        # Update Partner record
        if 'address_line1' in vals:
            line1 = vals['address_line1'].strip()
            vals.update({'address_line1': line1, 'street':line1})
            # vals.update({'street': vals['address_line1']})

        if 'address_line2' in vals:
            line2 = vals['address_line2'].strip()
            vals.update({'street2': line2, 'address_line2': line2})

        if 'town' in vals:
            twn = vals['town'].strip()
            vals.update({'city': twn, 'town': twn})

        if 'province' in vals:
            prvn = vals['province'].strip()
            vals.update({'province': prvn})

        if 'nation' in vals:
            cntry = vals['nation'].strip()
            vals.update({'nation': cntry})

        # Get student ID
        vals['stu_reg_number'] = self.pool.get('ir.sequence').get(cr, uid, 'myschool.op_student') or '/'
        vals.update({'is_student': True})  # Partner type is student
        # vals.update({'stu_reg_id': vals['stu_reg_number']})  # Support backwards compatible

        # email validation on create
        if 'email' in vals:
            self.validate_email(cr, uid, [], vals['email'])

        # NIC validation on create
        if 'id_number' in vals:
            self.validate_NIC(cr, uid, [], vals['id_number'])

        # Save student and get record id
        stu_id = super(op_student, self).create(cr, uid, vals, context=context)

        # Many to Many course logic
        course_map_ref = self.pool.get('op.student.batch.mapping')  # get reference to object
        # Validate Course mandatory
        course_count = course_map_ref.search(cr, uid, [('student_id', '=', stu_id)], count=True, context=context)
        if course_count < 1:
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
                                       'def_batch': def_course[0].batch_id.id,
                                       'def_standard': def_course[0].standard_id.id, }, context=context)
        return stu_id

    def write(self, cr, uid, ids, values, context=None):
        # email validation on write
        if 'email' in values:
            self.validate_email(cr, uid, ids, values['email'])

        # # NIC validation on write
        if 'id_number' in values:
            self.validate_NIC(cr, uid, ids, values['id_number'])

        # phone number validation on write
        if 'phone' in values:
            self.phoneNumberValidation(cr, uid, [], values['phone'])
        if 'contact_no' in values:
            self.phoneNumberValidationParent(cr, uid, [], values['contact_no'])

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

        if 'address_line1' in values:
            line1 = values['address_line1'].strip()
            values.update({'street': line1, 'address_line1': line1})

        if 'address_line2' in values:
            line2 = values['address_line2'].strip()
            values.update({'street2': line2, 'address_line2': line2})

        if 'town' in values:
            twn = values['town'].strip()
            values.update({'city': twn, 'town': twn})

        if 'province' in values:
            prvn = values['province'].strip()
            values.update({'province': prvn})

        if 'nation' in values:
            cntry = values['nation'].strip()
            values.update({'nation': cntry})

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
                                                             'def_batch': setmap.batch_id.id,
                                                             'def_standard': setmap.standard_id.id,}, context=context)
                return True

        return super(op_student, self).write(cr, uid, ids, values, context=context)

    def _check_birthday(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            date_birth_day = obj.birth_date
            date_today = date.today()
            if date_birth_day and date_today:
                datetime_format = "%Y-%m-%d"
                bday = datetime.strptime(date_birth_day, datetime_format)
                tday = datetime.strptime(date_today.strftime('%Y%m%d'), '%Y%m%d')
                if tday < bday:
                    return False
                return True

    # Related to the show Payment Schedule lines for particular student
    def show_payment_details(self, cr, uid, ids, context=None):
        stu_ps_id_list = []
        stu_id = ids[0]
        ps_obj = self.pool.get('op.payment.schedule')
        stu_ps_id_list = ps_obj.search(cr, uid, [('student_id', '=', stu_id)])
        # check already created a  payment schedule
        if len(stu_ps_id_list) == 0:
            raise osv.except_osv(_('No payment schedule'), _('You have not create a payment schedule for the student yet'))
        else:
            domain = [('schedule_id', '=', stu_ps_id_list)]

        return {
            'name': 'Payment Schedule Line',
            'view_mode': 'tree',
            'view_type': 'tree',
            'res_model': 'op.payment.schedule.line',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'domain': domain,
            }


    def create_invoice(self, cr, uid, ids, context={}):
        """ Create invoice for fee payment process of student """

        invoice_pool = self.pool.get('account.invoice')

        default_fields = invoice_pool.fields_get(cr, uid, context=context)
        invoice_default = invoice_pool.default_get(cr, uid, default_fields, context=context)

        for student in self.browse(cr, uid, ids, context=context):

            onchange_partner = invoice_pool.onchange_partner_id(cr, uid, [], type='out_invoice', \
                                partner_id=student.partner_id.id)
            invoice_default.update(onchange_partner['value'])


            invoice_data = {
                            'partner_id': student.partner_id.id,
                            'date_invoice': time.strftime('%Y-%m-%d'),
                            # 'payment_term': student.standard_id.payment_term and student.standard_id.payment_term.id or student.course_id.payment_term and student.course_id.payment_term.id or False,
                            }

        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(cr, uid, invoice_default, context=context)

        models_data = self.pool.get('ir.model.data')
        form_view = models_data.get_object_reference(cr, uid, 'account', 'invoice_form')
        tree_view = models_data.get_object_reference(cr, uid, 'account', 'invoice_tree')
        value = {
                'domain': str([('id', '=', invoice_id)]),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'view_id': False,
                'views': [(form_view and form_view[1] or False, 'form'),
                          (tree_view and tree_view[1] or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': invoice_id,
                'target': 'current',
                'nodestroy': True
            }
        return value



    _constraints = [
        (_check_birthday, 'Birth Day cannot be future date!', ['birth_date']),
        (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
        (_check_add_l_one, 'Entered Invalid Data in Address !!', ['address_line1']),
        (_check_add_l_two, 'Entered Invalid Data in Address !!', ['address_line2']),
        (_check_town, 'Entered Invalid Data in Address !!', ['town']),
        (_check_province, 'Entered Invalid Data in Address !!', ['province']),
        (_check_nation, 'Entered Invalid Data in Address !!', ['nation']),
    ]


    # def fnct_search(self, cr, uid, op_student_batch_mapping, name, args):
    #     all_batches = self.pool.get('op.student.batch.mapping')
    #     batch_ids = all_batches.browse(cr, uid, )
    #     return







