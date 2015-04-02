from openerp.osv import osv, fields
import datetime


class op_batch(osv.Model):

    _name = 'op.batch'
    _columns = {
        'name': fields.char(size=25, string='Name', required=True),
        'code': fields.char(size=15, string='Code', required=True),
        'start_date': fields.date(size=15, string='Start Date', required=True),
        'end_date': fields.date(size=15, string='End Date', required=True, onchange="validate_date_range"),
        'state': fields.selection(
            [('planned', 'Planned'), ('running', 'Running'), ('cancel', 'Cancel'), ('finished', 'finished')],
            string='State'),
        'course_id': fields.many2one('op.course', string='Course', ondelete='restrict', required=True),
    }

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Batch must be unique!')]

    def _check_date(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            start_date = obj.start_date
            end_date = obj.end_date
            if start_date and end_date:
                datetime_format = "%Y-%m-%d"  ## Set your date format here
                from_dt = datetime.datetime.strptime(start_date, datetime_format)
                to_dt = datetime.datetime.strptime(end_date, datetime_format)
                if to_dt < from_dt:
                    return False
                return True

    _constraints = [
        (_check_date, 'End Date should be greater than Start Date!', ['start_date', 'end_date']),
    ]

    _defaults = {
        'state': 'planned',
    }



