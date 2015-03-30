from openerp.osv import osv, fields


class op_subject(osv.Model):
    _name = 'op.subject'
    _columns = {
        'name': fields.char(size=50, string='Name', required=True),
        'code': fields.char(size=25, string='Code', required=True),
        # 'type': fields.selection([('t', 'Theory'), ('p', 'Practical'),  ('pt','Both'), ('o', 'Other')], string='Type'),
        'type': fields.selection([('core', 'Core'), ('elective', 'Elective')], string='Type'),
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        # 'subject_ids': fields.many2one('op.student.sub.map', 'Subject map')

    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the SUBJECT must be unique!')]


