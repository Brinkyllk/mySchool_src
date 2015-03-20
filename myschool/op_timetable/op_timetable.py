from osv import osv
from osv import fields


class op_period(osv.osv):
    _name = 'op.period'
    _description = 'Period'
    _order = "sequence"

    _columns = {
        'name': fields.char('Name', size=16, required=True),
        'hour': fields.selection([('1', '1'), ('2', '2'), ('3', '3'),
                                  ('4', '4'), ('5', '5'), ('6', '6'),
                                  ('7', '7'), ('8', '8'), ('9', '9'),
                                  ('10', '10'), ('11', '11'), ('12', '12'),
                                  ], 'Hours', required=True),

        'minute': fields.selection([('00', '00'), ('15', '15'),
                                    ('30', '30'), ('45', '45'),
                                    ], 'Minute', required=True),

        'duration': fields.float('Duration'),
        'am_pm': fields.selection([('am', 'AM'), ('pm', 'PM')], 'AM/PM', required=True),
        'sequence': fields.integer('Sequence'),
    }


op_period()


class op_timetable(osv.osv):
    _name = 'op.timetable'
    _description = 'Time Table'
    _rec_name = 'lecturer_id'

    _columns = {
        'period_id': fields.many2one('op.period', 'Period', required=True),
        'start_datetime': fields.datetime('Start', required=True),
        'end_datetime': fields.datetime('End', required=True),
        'lecturer_id': fields.many2one('op.lecturer', 'Lecturer', required=True),
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'classroom_id': fields.many2one('op.classroom', 'Classroom', readonly=True),
        'subject_id': fields.many2one('op.subject', 'Subject', required=True),
        'color': fields.integer('Color Index'),
        'type': fields.selection(
            [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
             ('Friday', 'Friday'), ('Saturday', 'Saturday')], 'Days'),
    }


op_timetable()
