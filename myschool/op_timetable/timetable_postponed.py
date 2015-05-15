from openerp.osv import osv, fields


class op_payment_schedule_line(osv.Model):
    _name = 'timetable.postponed'
    _columns = {
        'timetable_id': fields.many2one('op.period'),
        'period_id': fields.many2one('op.period', 'Period'),
        'classroom_id': fields.many2one('op.classroom', 'Classroom'),
        'date': fields.date('Date'),
    }
