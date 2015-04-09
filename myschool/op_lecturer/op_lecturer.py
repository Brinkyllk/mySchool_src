from openerp.osv import osv, fields
from datetime import date, datetime
import re


class op_lecturer(osv.Model):

    def validate_email(self, cr, uid, ids, email):
        if email is False:
            return True
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email)== None:
            raise osv.except_osv('Invalid Email', 'Please enter a valid email address')
        return True

    _name = 'op.lecturer'
    _inherits = {'res.partner': 'partner_id'}

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, ondelete="restrict"),
        'birth_date': fields.date(string='Birth Date', required=True),
        'category': fields.selection([('parttime', 'Part Time'), ('visiting', 'Visiting'), ('fulltime', 'Full Time')], string='Category', required=True),
        'gender': fields.selection([('m','Male'),('f','Female')], string='Gender', required=True),
        'language': fields.selection([('sinhala', 'Sinhala'), ('english', 'English'), ('tamil', 'Tamil')], string='Language'),
        'bank_acc_num': fields.char(size=64, string='Bank Acc Number'),
        'lecturer_subject_ids': fields.many2many('op.subject', 'lecturer_subject_rel', 'op_lecturer_id', 'op_subject_id', string='Subjects'),
        # 'mobile_no': fields.char(size=15, string='Mobile Number', required=True),

    }

    _sql_constraints = [('name', 'UNIQUE (name)', 'The Lecturer  must be unique!')]

    # overriding create method
    def create(self, cr, uid, vals, context=None):
        vals.update({'supplier': True, 'customer': False})
        if 'email' in vals:
            self.validate_email(cr, uid, [], vals['email'])
        res = super(op_lecturer, self).create(cr, uid, vals, context=context)
        return res

    # overriding write method
    def write(self, cr, uid, ids, values, context=None):
        if 'email' in values:
            self.validate_email(cr, uid, ids, values['email'])
            res = super(op_lecturer, self).write(cr, uid, ids, values, context=context)
            return res

    def _check_birthday(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            print "OK"
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



