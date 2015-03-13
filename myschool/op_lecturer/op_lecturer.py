from openerp.osv import osv, fields

class op_lecturer(osv.Model):
    _name = 'op.lecturer'
    _inherits = {'res.partner': 'partner_id'}

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, ondelete="restrict"),
        'birth_date': fields.date(string='Birth Date', required=True),
        'category': fields.selection([('fulltime', 'Full Time'), ('visiting', 'Visiting'), ('parttime', 'Part Time')], string='Category'),
        'gender': fields.selection([('m','Male'),('f','Female')], string='Gender', required=True),
        'language': fields.selection([('sinhala', 'Sinhala'), ('english', 'English'), ('tamil', 'Tamil')], string='Language'),
        'bank_acc_num': fields.char(size=64, string='Bank Acc Number'),
        'lecturer_subject_ids': fields.many2many('op.subject', 'lecturer_subject_rel', 'op_lecturer_id', 'op_subject_id', string='Subjects'),


    }

