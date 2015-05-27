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
        'birth_date': fields.date(string='Birth Date', required=True),
        'category': fields.selection([('parttime', 'Part Time'), ('visiting', 'Visiting'), ('fulltime', 'Full Time')],
                                     string='Category', required=True),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female')], string='Gender', required=True),
        'language': fields.selection([('sinhala', 'Sinhala'), ('english', 'English'), ('tamil', 'Tamil')],
                                     string='Language'),
        'bank_acc_num': fields.char(size=64, string='Bank Acc Number'),
        'lecturer_subject_ids': fields.many2many('op.subject', 'lecturer_subject_rel', 'op_lecturer_id',
                                                 'op_subject_id', string='Subjects'),
        'phone': fields.char(string='Phone Number', size=256),
        'id_number': fields.char(size=10, string='NIC', required=True),
        # 'mobile_no': fields.char(size=15, string='Mobile Number', required=True),
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
    ]



