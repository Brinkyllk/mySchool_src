from openerp.osv import osv, fields
from datetime import date, datetime
import re
from validate_email import validate_email
from openerp.tools.translate import _


class op_lecturer(osv.Model):
    def validate_email(self, cr, uid, ids, email):
        if email is False:
            return True
        is_valid = validate_email(email)
        if is_valid is False:
            raise osv.except_osv('Invalid Email', 'Please enter a valid email address')
        return True

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
        'birth_date': fields.date(string='Birth Date / Registered Date', required=True),
        'category': fields.selection([('parttime', 'Part Time'), ('visiting', 'Visiting'), ('fulltime', 'Full Time')],
                                     string='Category', required=True),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female')], string='Gender', required=True),
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
        'id_number': fields.char(size=10, string='NIC', required=True),
        # 'mobile_no': fields.char(size=15, string='Mobile Number', required=True),
    }

    _defaults = {
       'gender': 'm'
    }

    _sql_constraints = [('bank_acc_num', 'UNIQUE (bank_acc_num)', 'Bank Acc Number  must be unique!'),
                        ('id_number', 'UNIQUE (id_number)', 'The NIC  of the Student  must be unique!')
    ]

    def validate_NIC(self, cr, uid, ids, id_number):
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

        res = super(op_lecturer, self).write(cr, uid, ids, values, context=context)
        return res

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

    _constraints = [
        (_check_birthday, 'Birth Day cannot be future date!', ['birth_date']),
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


