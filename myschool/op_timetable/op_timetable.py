from openerp.osv import osv
from openerp.osv import fields
from openerp import netsvc


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

    def _check_duration(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            time_duration = obj.duration
            if time_duration < 1:
                return False
            else:
                return True

    _constraints = [
        (_check_duration,'Duration cannot be lower than one hour', ['duration']),
    ]


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
        'classroom_id': fields.many2one('op.classroom', 'Classroom', required=True),
        'subject_id': fields.many2one('op.subject', 'Subject', required=True),
        'color': fields.integer('Color Index'),
        'type': fields.selection(
            [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
             ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], 'Days'),
        'state': fields.selection([('planned', 'Planned'),
                                   ('completed', 'Completed'),
                                   ('postponed', 'Postponed'),
                                   ('cancelled', 'Cancelled')], readonly=True, string='State'),
    }

    _defaults = {
        'state': 'planned',
    }

    def onchange_lecturer(self, cr, uid, lecturer_id):
        lecturer = lecturer_id
        related_records = self.pool.get('lecturer_subject_rel').browse(cr, uid, [('op_lecturer_id', '=', lecturer)])
        related_subjects = related_records.op_subject_id
        subject_ids = self.pool.get('op.subject').browse(cr, uid, [('subject_id', '=', related_subjects)])
        return{'value': {'subject_id': subject_ids}}

    def action_planned(self, cr, uid, ids, context=None):
        # wf_service = netsvc.LocalService("workflow")
        self.write(cr, uid, ids, {'state': 'planned'})
        # for inv_id in ids:
            # wf_service.trg_delete(uid, 'op.timetable', inv_id, cr)
            # wf_service.trg_create(uid, 'op.timetable', inv_id, cr)
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancelled'})
        return True

    def action_postponed(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'postponed'})
        return True

    def action_complete(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'completed'})
        return True


op_timetable()
