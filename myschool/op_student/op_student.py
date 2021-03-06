from openerp.osv import fields, osv
from datetime import date, datetime
from openerp.tools.translate import _
import re
from openerp import api
import time


class op_student(osv.Model):

    @api.onchange('enrollment_ids')
    def onchange_enroll(self, cr, uid, ids, enrollment_ids):
        exist_ids = enrollment_ids[0][2]
        len_list = len(enrollment_ids)-1
        a = enrollment_ids[1:]
        for i in a:
            b = i[2].get('batch_code')
            for x in exist_ids:
                batch_code = self.pool.get('op.enrollment').read(cr, uid, x, ['batch_code']).get('batch_code')[0]
                if b == batch_code:
                    raise osv.except_osv(_('Error'), _('Please delete the duplicated Enrollments'))
        return True




    # --Code change to upper case---
    @api.onchange('initials')
    def onchange_case(self, cr, uid, ids, initials):
        if initials != False:
            result = {'value': {
                'initials': str(initials).upper()
            }
            }
            return result
        else:
            return True

    #--First name first letter capitalization---
    @api.onchange('first_name')
    def onchange_fname(self, cr, uid, ids, first_name):
        if first_name != False:
            result = {'value': {
                'first_name': str(first_name).title()
            }
            }
            return result
        else:
            return True

    #--Last name first letter capitalization---
    @api.onchange('last_name')
    def onchange_lname(self, cr, uid, ids, last_name):
        if last_name != False:
            result = {'value': {
                'last_name': str(last_name).title()
            }
            }
            return result
        else:
            return True

    #--Middle name first letter capitalization---
    @api.onchange('middle_name')
    def onchange_mname(self, cr, uid, ids, middle_name):
        if middle_name != False:
            result = {'value': {
                'middle_name': str(middle_name).title()
            }
            }
            return result
        else:
            return True

    #When add a NIC auto generate the BirthDate
    @api.onchange('id_number')
    def onchange_nic(self, cr, uid, ids, id_number):
        if id_number == False:
            result = {'value': {
                'id_number': str(id_number).upper()
            }}
        elif re.match('^\d{9}(X|V|v|x)$', id_number) == None:
            raise osv.except_osv('Invalid NIC', 'Please enter a valid NIC')
        else:
            id = str(id_number)
            year = id[0:2]
            newYear = int(year)
            newYear += 1900

            character = (int(id[2:5]))
            getdays = 0
            getmonth = 0

            if character >= 501 and character <= 866 or character >= 1 and character <= 366:
                if character >= 501 and character <= 866:
                    getdays = character - 500
                elif character >= 1 and character <= 366:
                    getdays = character

                for i in (31,29,31,30,31,30,31,31,30,31,30,31):
                    getmonth = getmonth + 1
                    if getdays <= i:
                        day = int(getdays)
                        month = int(getmonth)
                        break
                    else:
                        getdays = getdays - i
                fdate = date(newYear,month,day)

                result = {'value': {'birth_date': fdate, 'id_number': str(id_number).upper()}}
                return result
            else:
                raise osv.except_osv('Invalid NIC', 'Please enter a valid NIC')

    #onchange for is_company
    @api.multi
    def onchange_type(self, is_company):
        value = {'title': False}
        if is_company:
            value['use_parent_address'] = False
            domain = {'title': [('domain', '=', 'partner')]}
            value['gender'] = 'o'
        else:
            domain = {'title': [('domain', '=', 'contact')]}
        return {'value': value, 'domain': domain}


    _name = 'op.student'
    _description = 'Student'

    _inherits = {'res.partner': 'partner_id',}

    _columns = {
        #------ personal details ------
        'title': fields.many2one('res.partner.title', 'Title'),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, ondelete="restrict", readonly=True),
        'initials': fields.char(size=20, string='Initials'),
        'first_name': fields.char(size=15, string='First Name', required=True, select=True),
        'middle_name': fields.char(size=15, string='Middle Name'),
        'last_name': fields.char(size=20, string='Last Name', required=True, select=True),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', required=True),
        'birth_date': fields.date(string='Birth Date'),
        'register_date': fields.date(string='Registered Date'),
        'nationality': fields.many2one('res.country', string='Nationality test'),
        'language': fields.many2one('res.lang', string='Mother Tongue'),
        'id_number': fields.char(size=10, string='NIC'),
        #'photo': fields.related('partner_id', 'image', string='Photo', type='binary', readonly=True),
        'emails': fields.char(string='Email', size=128),
        'phone': fields.char(string='Phone Number', size=12),

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

        #------ Map many Courses ------
        # 'batch_ids': fields.one2many('op.student.batch.mapping', 'student_id', string='Registered Courses'),
        'enrollment_ids': fields.one2many('op.enrollment', 'student_id', string='Registered Courses'),

        #payment schedule
        'payment_schedule_id': fields.one2many('op.payment.schedule', 'student_id', 'Payment Schedules'),
        'registration_id': fields.integer('Registration Id'),

    }

    _defaults = {
       'gender': 'm'
    }

    _sql_constraints = [('id_number', 'UNIQUE (id_number)', 'The NIC  of the Student  must be unique!')]

    def default_get(self, cr, uid, fields, context=None):
        data = super(op_student, self).default_get(cr, uid, fields, context=context)
        # global activeId
        # activeId = context.get('active_id')
        regId = context.get('id')
        if regId:

            registrationRef = self.pool.get('op.registration')
            enrollmentRef = self.pool.get('op.enrollment')
            registrationId = registrationRef.browse(cr, uid, regId, context=context)
            enrollmentId = enrollmentRef.search(cr, uid, [('reg_id', '=', regId)])

            data['image'] = registrationId.photo
            data['initials'] = registrationId.initials
            data['first_name'] = registrationId.first_name
            data['middle_name'] = registrationId.middle_name
            data['last_name'] = registrationId.last_name
            data['birth_date'] = registrationId.birth_date
            data['gender'] = registrationId.gender
            data['photo'] = registrationId.photo
            data['address_line1'] = registrationId.address_line1
            data['address_line2'] = registrationId.address_line2
            data['town'] = registrationId.town
            data['province'] = registrationId.province
            data['nation'] = registrationId.nation
            data['enrollment_ids'] = enrollmentId
            data['registration_id'] = regId

        return data

    def _check_nic(self, nic):
        pass

    #Can not delete all the enrollments of the specific student
    def _canNotDeleteEnrollments(self, cr, uid, ids, context=None):
        studentEnrollmentMapRef = self.pool.get('op.enrollment')
        enrollmentMapId = studentEnrollmentMapRef.search(cr,uid, [('student_id', 'in', ids)])
        lenEnrollmentMapId = len(enrollmentMapId)
        if lenEnrollmentMapId == 0:
            return False
        else:
            return True

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


    # #..... check passing nul values....#
    # def _check_invalid_data(self, cr, uid, ids, context=None):
    #     obj = self.browse(cr, uid, ids, context=context)
    #     initials = str(obj.initials)
    #     fnew_name = str(obj.first_name)
    #     middle_name = str(obj.middle_name)
    #     lnew_code = str(obj.last_name)
    #     initials = initials.replace(" ","")
    #     new_ini = initials.replace("." ,"")
    #     fname = fnew_name.replace(" ", "")
    #     mname = middle_name.replace(" ","")
    #     lname = lnew_code.replace(" ", "")
    #     #isalpha python inbuilt function Returns true if string
    #         #has at least 1 character and all characters are alphabetic and false otherwise.
    #     if fname :
    #         if fname.isalpha():
    #             return True
    #             if mname.isalpha():
    #                 return True
    #                 if lname.isalpha():
    #                     return True
    #                     if new_ini.isalpha():
    #                         return True
    #         else:
    #             return False
    #     else:
    #         return False

    # email validation........
    def validate_emails(self, cr, uid, ids, emails):
        email = re.compile("^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$")
        valid_emails = False
        if emails is False:
            return True
        if email.match(emails):
            valid_emails=True
            return True
        else:
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid Email'))

    # ---initials validation written by s----- #
    def validate_initials(self,cr, uid, ids, initials):
        ini = str(initials).replace(" ", "")
        ini = ini.replace(".", "")
        if ini.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Initials'), _('Enter Initials Correctly'))

    # ----first name validation written by s--- #
    def validate_first_name(self, cr, uid, ids, first_name):
        f_name = str(first_name).replace(" ", '')
        if f_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid First Name'), _('Please enter valid First name'))

    # ----last name validation written by s--- #
    def validate_last_name(self, cr, uid, ids, last_name):
        l_name = str(last_name).replace(" ", "")
        if l_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Last Name'), _('Please enter valid Last name'))

    # -----middle name validation written by s--- #
    def validate_middle_name(self, cr, uid, ids, middle_name):
        m_name = str(middle_name).replace(" ", "")
        if m_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Middle Name'), _('Please enter a valid Middle Name'))

    def validate_NIC(self, cr, uid, ids, id_number):
        if id_number is None:
            return True
        if id_number is False:
            return True
        if re.match('^\d{9}(X|V)$', id_number) is None:
            raise osv.except_osv('Invalid NIC', 'Please enter a valid NIC')
        return True

    # phone number validation for student
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

    # phone number validation for parent
    def phoneNumberValidationParent(self, cr, uid, ids, phoneNumber):
        phone_re = re.compile(ur'^(\+\d{1,1}[- ]?)?\d{10}$')
        # valid_phone = False
        if phoneNumber is False:
            return True
        if phone_re.match(phoneNumber):
            # valid_phone=True
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
        # vals = self.browse(cr, uid, ids, context=context)
        if 'first_name' in vals:
            fname = vals['first_name'].strip()
            vals.update({'first_name': fname})

        if 'middle_name' in vals:
            if vals['middle_name'] is False or None:
                pass
            else:
                mi_name = vals['middle_name'].strip()
                vals.update({'middle_name': mi_name})

        if 'last_name' in vals:
            lname = vals['last_name'].strip()
            vals.update({'last_name': lname})

        if 'initials' in vals:
            if vals['initials'] is False or None:
                pass
            else:
                initls = vals['initials'].strip()
                vals.update({'initials': initls})

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

        # Fix initials if empty....
        try:
            initials = vals['initials'].strip()
        except Exception:
            initials = ''
            pass

        if 'first_name' in vals:
            if initials == '':
                full_name = vals['first_name'].strip() + ' ' + vals['last_name'].strip()
            else:
                full_name = vals['initials'] + ' ' + vals['first_name'].strip() + ' ' + vals['last_name'].strip()
            vals.update({'name': full_name})  # Update Partner record

        # Address lines and update res.partner
        if 'address_line1' in vals:
            if vals['address_line1'] is False or None:
                pass
            else:
                line1 = vals['address_line1'].strip()
                vals.update({'street': line1, 'address_line1': line1})

        if 'address_line2' in vals:
            if vals['address_line2'] is False or None:
                pass
            else:
                line2 = vals['address_line2'].strip()
                vals.update({'street2': line2, 'address_line2': line2})

        if 'town' in vals:
            if vals['town'] is False or None:
                pass
            else:
                twn = vals['town'].strip()
                vals.update({'city': twn, 'town': twn})

        if 'province' in vals:
            if vals['province'] is False or None:
                pass
            else:
                prvn = vals['province'].strip()
                vals.update({'province': prvn})

        if 'nation' in vals:
            if vals['nation'] is False or None:
                pass
            else:
                cntry = vals['nation'].strip()
                vals.update({'nation': cntry})

        # Get student ID
        vals['stu_reg_number'] = self.pool.get('ir.sequence').get(cr, uid, 'myschool.op_student') or '/'
        vals.update({'is_student': True})  # Partner type is student
        vals.update({'stu_reg_id': vals['stu_reg_number']})  # Support backwards compatible

        # email validation on create
        if 'emails' in vals:
            self.validate_emails(cr, uid, [], vals['emails'])
            vals.update({'email': vals['emails']})

        # ----validator caller written by s-- #
        if 'last_name' in vals:
            self.validate_last_name(cr, uid, [], vals['last_name'])

        # ----validator caller written by s-- #
        if 'first_name' in vals:
            self.validate_first_name(cr, uid, [], vals['first_name'])

        # ----validator caller written by s-- #
        if 'middle_name' in vals:
            self.validate_middle_name(cr, uid, [], vals['middle_name'])

        # ----validator caller written by s-- #
        if 'initials' in vals:
            self.validate_initials(cr, uid, [], vals['initials'])

        # NIC validation on create
        if 'id_number' in vals:
            self.validate_NIC(cr, uid, [], vals['id_number'])

        # if 'is_company' in vals:
        #     if vals['is_company'] == True:
        #         if vals['register_date'] == False or vals['register_date'] == None:
        #             raise osv.except_osv('Error', 'Registered Date cannot be null..!!')
        #     else:
        #         if vals['birth_date'] == False or vals['birth_date'] == None:
        #             raise osv.except_osv('Error', 'Birth Date cannot be null..!!')


        #-----Check whether enrollment has or not-------#
        # stu_id = super(op_student, self).create(cr, uid, vals, context=context)
        # enrollment_ref = self.pool.get('op.enrollment')
        # enrollment_count = enrollment_ref.search(cr, uid, [('student_id', '=', stu_id)], count=True, context=context)
        # if enrollment_count < 1:
        #     raise osv.except_osv(_(u'Error'), _(u'Make an Enrollment'))
        #     return

        # # write to the registration form
        # registrationRef = self.pool.get('op.registration')
        # registrationRef.write(cr, uid, { 'student_id': activeId})

        if 'registration_id' in vals:
            reg_id = vals['registration_id']
            reg_ref = self.pool.get('op.registration')
            reg_ref.write(cr, uid, [reg_id], {'state': 'done'})

        return super(op_student, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, values, context=None):
        if 'initials' in values:
            if values['initials'] is False or None:
                pass
            else:
                initls = values['initials'].strip()
                values.update({'initials': initls})

        if 'first_name' in values:
            fname = values['first_name'].strip()
            values.update({'first_name': fname})

        if 'middle_name' in values:
            if values['middle_name'] is False or None:
                pass
            else:
                mi_name = values['middle_name'].strip()
                values.update({'middle_name': mi_name})

        # email validation on write
        if 'emails' in values:
            self.validate_emails(cr, uid, ids, values['emails'])
            values.update({'email': values['emails']})

        # # NIC validation on write
        if 'id_number' in values:
            self.validate_NIC(cr, uid, ids, values['id_number'])

        # phone number validation on write
        if 'phone' in values:
            self.phoneNumberValidation(cr, uid, [], values['phone'])
        if 'contact_no' in values:
            self.phoneNumberValidationParent(cr, uid, [], values['contact_no'])

        # ----validator caller written by s-- #
        if 'initials' in values:
            self.validate_initials(cr, uid, [], values['initials'])

        # ----validator caller written by s-- #
        if 'first_name' in values:
            self.validate_first_name(cr, uid, [], values['first_name'])

        # ----validator caller written by s-- #
        if 'middle_name' in values:
            self.validate_middle_name(cr, uid, [], values['middle_name'])

        # ----validator caller written by s-- #
        if 'last_name' in values:
            self.validate_last_name(cr, uid, [], values['last_name'])

        # clean NIC
        if 'id_number' in values:
            try:
                values['id_number'] = values['id_number'].strip()
                if values['id_number'] == '':
                    values['id_number'] = None
            except:
                values['id_number'] = None

        # -------- Update Partner record -------------
        exstu = self.browse(cr, uid, ids, context=context)
        ini = exstu.initials
        firstName = exstu.first_name
        lastName = exstu.last_name
        global initial

        if 'initials' in values:
            if values['initials'] is False or None:
                initial = ''
            else:
                initial = values['initials']
        else:
            if ini is False or None:
                initial = ''
            else:
                initial = ini

        if 'first_name' in values:
            fName = values['first_name']
        else:
            fName = firstName

        if 'last_name' in values:
            lName = values['last_name']
        else:
            lName = lastName

        if initial == '':
            full_name = fName.strip() + ' ' + lName.strip()
        else:
            full_name = initial.strip() + ' ' + fName.strip() + ' ' + lName.strip()
        values.update({'name': full_name})

        # -------- Update Partner record -------------
        if 'address_line1' in values:
            if values['address_line1'] is False or None:
                pass
            else:
                line1 = values['address_line1'].strip()
                values.update({'street': line1, 'address_line1': line1})

        if 'address_line2' in values:
            if values['address_line2'] is False or None:
                pass
            else:
                line2 = values['address_line2'].strip()
                values.update({'street2': line2, 'address_line2': line2})

        if 'town' in values:
            if values['town'] is False or None:
                pass
            else:
                twn = values['town'].strip()
                values.update({'city': twn, 'town': twn})

        if 'province' in values:
            if values['province'] is False or None:
                pass
            else:
                prvn = values['province'].strip()
                values.update({'province': prvn})

        if 'nation' in values:
            if values['nation'] is False or None:
                pass
            else:
                cntry = values['nation'].strip()
                values.update({'nation': cntry})


        # if 'enrollment_ids' in values:
        #     stu = self.browse(cr, uid, ids, context).ids
        #     # ss = stu.ids[0]
        #     se = self.pool.get('op.enrollment')
        #     sa = se.search(cr, uid, [('student_id', '=', stu)], context=context)
        #     if len(sa) > 0:
        #         for id_no in sa:
        #             cr.execute('Delete from op_enrollment where student_id =%s' % (id_no))

        if 'enrollment_ids' in values:
            e =[]
            a = values['enrollment_ids']
            for b in a:
                c = b[2]
                if c is not False:
                    d = c.get('batch_code')
                    if d:
                        e.append(d)
                        f = e.count(d)
                        if f > 1:
                            raise osv.except_osv (_('Course Enrollment Error'), _('Enrollments cannot be duplicated'))
                        elif f == 1:
                            stu = self.browse(cr, uid, ids, context).ids
                            se = self.pool.get('op.enrollment')
                            sa = se.search(cr, uid, ['&', ('batch_code', '=', d), ('student_id', '=', stu)], context=context)
                            if len(sa) == 1:
                                # raise osv.except_osv(_('Error'), _('All ready Exist'))
                                cr.execute('Delete from op_enrollment where id =%s' % sa[0])

        return super(op_student, self).write(cr, uid, ids, values, context=context)

    def _check_registered_date(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            reg_day = obj.register_date
            if reg_day == False or reg_day == None:
                return True
            else:
                date_today = date.today()
                if reg_day and date_today:
                    datetime_format = "%Y-%m-%d"
                    rday = datetime.strptime(reg_day, datetime_format)
                    tday = datetime.strptime(date_today.strftime('%Y%m%d'), '%Y%m%d')
                    if tday < rday:
                        return False
                    return True

    def _check_birthday(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            date_birth_day = obj.birth_date
            if date_birth_day == False or date_birth_day ==None:
                return True
            else:
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
        (_check_registered_date, 'Registered Date cannot be future date!', ['register_date']),
        (_check_birthday, 'Birth Day cannot be future date!', ['birth_date']),
        # (_check_invalid_data, 'Entered Invalid Name Details!!', ['first_name']),
        (_check_add_l_one, 'Entered Invalid Data in Address line1 !!', ['address_line1']),
        (_check_add_l_two, 'Entered Invalid Data in Address line2 !!', ['address_line2']),
        (_check_town, 'Entered Invalid Data in City !!', ['town']),
        (_check_province, 'Entered Invalid Data in Province !!', ['province']),
        (_check_nation, 'Entered Invalid Data in Country !!', ['nation']),
        (_canNotDeleteEnrollments, 'Course Enrollment is Mandatory !!', ['enrollment_ids']),

    ]









