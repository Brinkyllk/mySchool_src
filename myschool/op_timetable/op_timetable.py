from openerp.osv import osv
from openerp.osv import fields
from openerp import api
from openerp import netsvc
import time
import datetime
import dateutil
from datetime import date
import calendar
from dateutil import parser


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
        'start_time': fields.float('Start Time'),
        'end_time': fields.float('End Time')
    }

    def create(self, cr, uid, vals, context=None):
        hours = float(vals['hour'])
        duration = vals['duration']
        minute = float(vals['minute'])
        val = minute / 60
        start_time = hours + val
        am_pm = vals['am_pm']
        if am_pm == 'pm':
            if hours == 12.00:
                pass
            else:
                start_time += 12.00
        end_time = start_time + duration
        vals.update({'start_time': start_time, 'end_time': end_time})
        return super(op_period, self).create(cr, uid, vals, context=context)

    def _check_duration(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            time_duration = obj.duration
            if time_duration == 0:
                return False
            else:
                return True

    _constraints = [
        (_check_duration, 'Duration cannot be zero hours', ['duration']),
    ]


op_period()


class op_timetable(osv.osv):
    _name = 'op.timetable'
    _description = 'Time Table'
    _rec_name = 'lecturer_id'

    _columns = {
        'period_id': fields.many2one('op.period', 'Period', required=True, readonly=True),
        'start_datetime': fields.datetime('Start', required=True, readonly=True),
        'end_datetime': fields.datetime('End', required=True, readonly=True),
        'lecturer_id': fields.many2one('op.lecturer', 'Lecturer', required=True, readonly=True),
        'standard_id': fields.many2one('op.standard', 'Standard', required=True, readonly=True),
        'classroom_id': fields.many2one('op.classroom', 'Classroom', required=True, readonly=True),
        'subject_id': fields.many2one('op.subject', 'Subject', required=True, readonly=True),
        'color': fields.integer('Color Index'),
        # 'type': fields.selection(
        #     [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
        #      ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], 'Days'),
        'type': fields.char('Days', readonly=True),
        'state': fields.selection([('planned', 'Planned'),
                                   ('completed', 'Completed'),
                                   ('postponed', 'Postponed'),
                                   ('cancelled', 'Cancelled')], readonly=True, string='State'),
    }

    _defaults = {
        'state': 'planned',
    }

    # @api.onchange('start_datetime')
    # def onchange_weekday(self):
    #     st_date = dateutil.parser.parse(self.start_datetime).date()
    #     day = calendar.day_name[st_date.weekday()]
    #     self.type = day

    #............checking the availability of the lecturer.......................#
    def _lecturer_conflict(self, cr, uid, ids, context=None):
        for self_object in self.browse(cr, uid, ids, context=context):
            start_date = dateutil.parser.parse(self_object.start_datetime).date()
            end_date = dateutil.parser.parse(self_object.end_datetime).date()
            lec_id = self_object.lecturer_id.id
            per_start = self_object.period_id.start_time
            per_end = self_object.period_id.end_time
            day = str(self_object.type)
            obj = self.pool.get("op.timetable").search(cr, uid, [('lecturer_id', '=', lec_id)])
            # obj_len = len(obj)-1
            # obj.pop(obj_len)
            print obj
            if obj:
                for record_id in obj:
                    details = self.pool.get('op.timetable').read(cr, uid, record_id, ['type', 'start_datetime', 'period_id'])
                    period_get = details.get('period_id')
                    period_get_id = period_get[0]
                    period_info = self.pool.get('op.period').read(cr, uid, period_get_id, ['start_time', 'end_time'])
                    period_info_start = period_info.get('start_time')
                    period_info_end = period_info.get('end_time')
                    day_type = str(details.get('type'))
                    if day_type == day:
                        asn_date = dateutil.parser.parse(details.get('start_datetime')).date()
                        if start_date <= asn_date <= end_date:
                            if per_start <= period_info_start < per_end or per_start < period_info_end <= per_end:
                                return False
            else:
                return True
        return True


    #...............checking the availability of the classroom................#
    def _classroom_conflict(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids, context=context):
            start_date = dateutil.parser.parse(self_obj.start_datetime).date()
            end_date = dateutil.parser.parse(self_obj.end_datetime).date()
            cls_id = self_obj.classroom_id.id
            per_start = self_obj.period_id.start_time
            per_end = self_obj.period_id.end_time
            day = str(self_obj.type)
            obj = self.pool.get("op.timetable").search(cr, uid, [('classroom_id', '=', cls_id)])
            obj_len = len(obj)-1
            obj.pop(obj_len)
            if obj:
                for rec_id in obj:
                    details = self.pool.get('op.timetable').read(cr, uid, rec_id, ['type', 'start_datetime', 'period_id'])
                    period_get = details.get('period_id')
                    period_get_id = period_get[0]
                    period_info = self.pool.get('op.period').read(cr, uid, period_get_id, ['start_time', 'end_time'])
                    period_info_start = period_info.get('start_time')
                    period_info_end = period_info.get('end_time')
                    day_type = str(details.get('type'))
                    if day_type == day:
                        asn_date = dateutil.parser.parse(details.get('start_datetime')).date()
                        if start_date <= asn_date <= end_date:
                            if per_start <= period_info_start < per_end or per_start < period_info_end < per_end:
                                return False

            else:
                return True
        return True

    #..................checking the availability of the standard..............#
    def _standard_conflict(self, cr, uid, ids, context=None):
        day_list = ['None', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for self_object in self.browse(cr, uid, ids, context=context):
            start_date = dateutil.parser.parse(self_object.start_datetime).date()
            end_date = dateutil.parser.parse(self_object.end_datetime).date()
            standard_id = self_object.standard_id.id
            per_start = self_object.period_id.start_time
            per_end = self_object.period_id.end_time
            day = str(self_object.type)
            obj = self.pool.get('op.timetable').search(cr, uid, [('standard_id', '=', standard_id), ], order=None)
            obj_len = len(obj)-1
            obj.pop(obj_len)
            if obj:
                for record_id in obj:
                    details = self.pool.get('op.timetable').read(cr, uid, record_id, ['type', 'start_datetime', 'period_id'])
                    period_get = details.get('period_id')
                    period_get_id = period_get[0]
                    period_info = self.pool.get('op.period').read(cr, uid, period_get_id, ['start_time', 'end_time'])
                    period_info_start = period_info.get('start_time')
                    period_info_end = period_info.get('end_time')
                    day_type = str(details.get('type'))
                    if day_type == day:
                        asn_date = dateutil.parser.parse(details.get('start_datetime')).date()
                        if start_date <= asn_date <= end_date:
                            if per_start <= period_info_start < per_end or per_start < period_info_end < per_end:
                                return False

            else:
                return True
        return True

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

    def _validate_backdate(self, cr, uid, ids, context=None):
        now = datetime.datetime.today()
        today = now.strftime('%Y-%m-%d')
        date_today = dateutil.parser.parse(today).date()
        for self_object in self.browse(cr, uid, ids, context=context):
            star_datetime = self_object.start_datetime
            obj_st_date = dateutil.parser.parse(star_datetime).date()
            if date_today > obj_st_date:
                return False
            return True
        return True
    _constraints = [#(_lecturer_conflict, 'Lecturer not available!!', ['start_datetime', 'end_datetime', 'period_id']),
                    #(_classroom_conflict, 'Classroom not available', ['classroom_id', 'period_id', 'start_datetime', 'end_datetime']),
                    #(_standard_conflict, 'Standard not available', ['standard_id', 'start_datetime', 'end_datetime']),
                    (_validate_backdate, 'You cannot backdate records!', ['start_datetime']),

                    ]


