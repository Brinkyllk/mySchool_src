from openerp.osv import osv, fields


class timetable_postponed(osv.osv_memory):
    _name = 'timetable.postponed'
    _columns = {
        'timetable_id': fields.many2one('op.period'),
        'period_id': fields.many2one('op.period', 'Period'),
        'classroom_id': fields.many2one('op.classroom', 'Classroom'),
        'date': fields.date('Date'),
    }