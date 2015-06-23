from openerp.osv import osv, fields
from openerp import api
from datetime import date, datetime
import re
from openerp.tools.translate import _



class op_lecturer(osv.Model):
    #lecturer name capitalization#
    @api.onchange('name')
    def onchange_name(self, cr, uid, ids, name):
        if name != False:
            result = {'value': {
                'name': str(name).title()
            }
            }
            return result
        else:
            return True

    # #lecturer nic capitalization
    # @api.onchange('id_number')
    # def onchange_name(self, cr, uid, ids, id_number):
    #     if id_number != False:
    #         result = {'value': {
    #             'name': str(id_number).upper()
    #         }
    #         }
    #         return result
    #     else:
    #         return True

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

    #Email validation
    def validate_email(self, cr, uid, ids, email):
        email_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")
        valid_email = False
        if email is False:
            return True
        if email_re.match(email):
            valid_email=True
            return True
        else:
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid Email'))

    #phone number validation for lecturer
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

    def validate_acc_num(self, cr, uid, ids, acc_num):
        if acc_num is False:
            return True
        if re.match("^[0-9]*$", acc_num) == None:
            raise osv.except_osv('Invalid Account No', 'Please enter a valid Account Number')
        return True

    _name = 'op.lecturer'
    _inherits = {'res.partner': 'partner_id'}

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, ondelete="restrict"),
        'birth_date': fields.date(string='Birth Date'),
        'register_date': fields.date(string='Registered Date'),
        'category': fields.selection([('parttime', 'Part Time'), ('visiting', 'Visiting'), ('fulltime', 'Full Time')],
                                     string='Category', required=True),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', required=True),
        'language': fields.selection([('sinhala', 'Sinhala'), ('english', 'English'), ('tamil', 'Tamil')],
                                     string='Language'),
        'bank': fields.selection([('BOC', 'Bank of Ceylon'), ('HSBC', 'HSBC'), ('Commercial Bank', 'Commercial Bank'),
                                  ('Sampath Bank', 'Sampath Bank'), ('Peoples Bank', 'Peoples Bank')], string='Bank'),
        'bank_acc_num': fields.char(size=64, string='Bank Acc Number'),

        'address_line1': fields.char('address line1', size=20),
        'address_line2': fields.char('address line2', size=25),
        'town': fields.char('town', size=25),
        'province': fields.char('province', size=20),
        'nation': fields.char('nation', size=20),

        'lecturer_subject_ids': fields.many2many('op.subject', 'lecturer_subject_rel', 'op_lecturer_id',
                                                 'op_subject_id', string='Subjects'),
        'phone': fields.char(string='Phone Number', size=256),
        'id_number': fields.char(size=10, string='NIC'),
        # 'mobile_no': fields.char(size=15, string='Mobile Number', required=True),
    }

    _defaults = {
       'gender': 'm'
    }

    _sql_constraints = [('bank_acc_num', 'UNIQUE (bank_acc_num)', 'Bank Acc Number  must be unique!'),
                        ('id_number', 'UNIQUE (id_number)', 'The NIC  of the Lecturer  must be unique!')
    ]

    def validate_NIC(self, cr, uid, ids, id_number, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.is_company)
        if id_number is None:
            return True
        if id_number is False:
            return True
        if re.match('^\d{9}(X|V)$', id_number) == None:
            raise osv.except_osv('Invalid NIC', 'Please enter a valid NIC')
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
        if not value or not new_value.isalpha():
            return False
        else:
            return True

    # overriding create method
    def create(self, cr, uid, vals, context=None):
        vals.update({'supplier': True, 'customer': False})

        # phone number validation on create
        if 'phone' in vals:
            self.phoneNumberValidation(cr, uid, [], vals['phone'])

        if 'email' in vals:
            self.validate_email(cr, uid, [], vals['email'])

        if 'bank_acc_num' in vals:
            self.validate_acc_num(cr, uid, [], vals['bank_acc_num'])

        # NIC validation on create
        if 'id_number' in vals:
            self.validate_NIC(cr, uid, [], vals['id_number'])

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

        if 'is_company' in vals:
            if vals['is_company'] == True:
                if vals['register_date'] == False or vals['register_date'] == None:
                    raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a Registered Date..!!')
            else:
                if vals['birth_date'] == False or vals['birth_date'] == None:
                    raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a NIC..!!')
                else:
                    if vals ['id_number'] == False or vals ['id_number'] == None:
                        raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a NIC..!!')

        res = super(op_lecturer, self).create(cr, uid, vals, context=context)
        return res

    # overriding write method
    def write(self, cr, uid, ids, values, context=None):
        # phone number validation on write
        if 'phone' in values:
            self.phoneNumberValidation(cr, uid, [], values['phone'])

        values.update({'supplier': True, 'customer': False})
        if 'email' in values:
            self.validate_email(cr, uid, ids, values['email'])

        if 'bank_acc_num' in values:
            self.validate_acc_num(cr, uid, [], values['bank_acc_num'])

        # NIC validation on create
        if 'id_number' in values:
            self.validate_NIC(cr, uid, [], values['id_number'])

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

        if 'is_company' in values:
            if values['is_company'] == True:
                if 'register_date' in values:
                    pass
                else:
                    raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a Registered Date..!!')
                    # if values['register_date'] == False or values['register_date'] == None:
                    #     raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a Registered Date..!!')
            else:
                if 'birth_date' in values:
                    if values['birth_date'] == False or values['birth_date'] == None:
                        raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a NIC..!!')
                    else:
                        if values['birth_date'] == False or values['birth_date'] == None:
                            raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a NIC..!!')
                        return True
                elif 'id_number' in values:
                    if values ['id_number'] == False or values ['id_number'] == None:
                        raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a NIC..!!')
                    else:
                        if values['id_number'] == False or values['birth_date'] == None:
                            raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a NIC..!!')
                        return True

        res = super(op_lecturer, self).write(cr, uid, ids, values, context=context)
        return res

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


    _constraints = [
        (_check_registered_date, 'Registered Date cannot be future date!', ['register_date']),
        (_check_add_l_one, 'Entered Invalid Data in Address line1 !!', ['address_line1']),
        (_check_add_l_two, 'Entered Invalid Data in Address line2 !!', ['address_line2']),
        (_check_town, 'Entered Invalid Data in City !!', ['town']),
        (_check_province, 'Entered Invalid Data in Province !!', ['province']),
        (_check_nation, 'Entered Invalid Data in Country !!', ['nation']),
    ]

# class op_lecturer_bank(osv.osv):
#     _name = 'op.lecturer.bank'
#     _order = 'name'
#     _columns = {
#         'name': fields.char('Bank', required=True, translate=True),
#         'shortcut': fields.char('Account Number', translate=True),
        # 'domain': fields.selection([('partner', 'Partner'), ('contact', 'Contact')], 'Domain', required=True)
    # }
    # _defaults = {
    #     'domain': 'contact',
    # }


