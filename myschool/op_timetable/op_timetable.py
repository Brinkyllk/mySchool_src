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

        'duration': fields.float('Duration', required=True),
        'am_pm': fields.selection([('am', 'AM'), ('pm', 'PM')], 'AM/PM', required=True),
        'sequence': fields.integer('Sequence'),
        'start_time': fields.float('Start Time'),
        'end_time': fields.float('End Time')
    }
    #.... check passing nul values..#
    def _check_invalid_data(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        new_name = str(obj.name)
        name = new_name.replace(" ", "")
        n_name = ''.join([i for i in name if not i.isdigit()])
        #isalpha python inbuilt function Returns true if string
            #has at least 1 character and all characters are alphabetic and false otherwise.
        if name:
            if n_name.isalpha() or name.isdigit():
                return True
        else:
            return False

    def create(self, cr, uid, vals, context=None):
        name = vals['name'].strip()
        vals.update({'name':name})
        #Start time & End Time calculation
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

    def write(self, cr, uid, ids,  values, context=None):
        if 'name' in values:
            name = values['name'].strip()
            values.update({'name': name})

        #Start time & End Time calculation
        ex_per = self.browse(cr, uid, ids, context=context)
        hr = ex_per.hour
        du = ex_per.duration
        min = ex_per.minute
        ex_am_pm = ex_per.am_pm

        if 'hour' in values:
            hours = float(values['hour'])
        else:
            hours = float(hr)

        if 'duration' in values:
            duration = values['duration']
        else:
            duration = du

        if 'minute' in values:
            minute = float(values['minute'])
        else:
            minute = float(min)

        if 'am_pm' in values:
            am_pm_val = values['am_pm']
        else:
            am_pm_val = ex_am_pm

        val = minute / 60
        start_time = hours + val

        if am_pm_val == 'pm':
            if hours == 12.00:
                pass
            else:
                start_time += 12.00
        end_time = start_time + duration

        values.update({'start_time': start_time, 'end_time': end_time})
        return super(op_period, self).write(cr, uid, ids,  values, context=context)

    def _check_duration(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            time_duration = obj.duration
            if time_duration == 0:
                return False
            else:
                return True

    def _check_period_time(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            id_info = obj.id
            hour_input = obj.hour
            minute_input = obj.minute
            am_pm_input = obj.am_pm
            duration_input = obj.duration
            new_obj = self.pool.get('op.period').search(cr, uid, [('hour', '=', hour_input)], order=None)
            for rec in new_obj:
                if id_info != rec:
                    get_data = self.pool.get('op.period').read(cr, uid, rec, ['minute', 'am_pm', 'duration'])
                    a = get_data.get('minute')
                    b = get_data.get('am_pm')
                    c = get_data.get('duration')
                    if a == minute_input and b == am_pm_input and c == duration_input:
                        return False
            return True

    _constraints = [
        (_check_duration, 'Duration cannot be zero hours', ['duration']),
        (_check_invalid_data, 'Entered Invalid Data!!', ['name']),
        (_check_period_time, "Period info cannot be duplicated",['hour'])
    ]

    _sql_constraints = [('name_unique','unique(name)', 'Period name must be unique!')]

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
    # def onchange_slot(start_datetime):
    #     raise osv.except_osv(('Error'), ('Click on the slot to change the slot' ) )
    #     return False

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

    _constraints = [
        (_validate_backdate, 'You cannot backdate records!', ['start_datetime']),
    ]


