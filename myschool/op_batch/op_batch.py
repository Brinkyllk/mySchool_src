from openerp.osv import osv, fields


class op_batch(osv.Model):
    _name = 'op.batch'
    _columns = {
        'name': fields.char(size=25, string='Name', required=True),
        'code': fields.char(size=15, string='Code', required=True),
        'start_date': fields.date(size=15, string='Start Date', required=True),
        'end_date': fields.date(size=15, string='End Date', required=True),
        'state': fields.selection(
            [('planned', 'Planned'), ('running', 'Running'), ('cancel', 'Cancel'), ('finished', 'finished')],
            string='State'),
        'course_id': fields.many2one('op.course', string='Course', ondelete='restrict', required=True)
        # 'standard_id': fields.many2one('op.standard', 'Standard', required=True),

    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Batch must be unique!')]

    _defaults = {
        'state': 'planned',
    }

