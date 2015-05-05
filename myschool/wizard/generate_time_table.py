from openerp.osv import osv
from openerp.osv import fields
import datetime
from .. import utils

week_number = {'Mon': 1,
               'Tue': 2,
               'Wed': 3,
               'Thu': 4,
               'Fri': 5,
               'Sat': 6,
               'Sun': 7,
               }


class generate_time_table(osv.osv_memory):
    _name = 'generate.time.table'
    _description = 'Generate Time Table'
    _rec_name = 'standard_id'

    _columns = {
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'classroom_id': fields.many2one('op.classroom', 'Classroom', required=True),
        'time_table_lines': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines', required=True),
        'time_table_lines_1': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines',
                                              domain=[('day', '=', '1')], required=True),
        'time_table_lines_2': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines',
                                              domain=[('day', '=', '2')], required=True),
        'time_table_lines_3': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines',
                                              domain=[('day', '=', '3')], required=True),
        'time_table_lines_4': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines',
                                              domain=[('day', '=', '4')], required=True),
        'time_table_lines_5': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines',
                                              domain=[('day', '=', '5')], required=True),
        'time_table_lines_6': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines',
                                              domain=[('day', '=', '6')], required=True),
        'time_table_lines_7': fields.one2many('gen.time.table.line', 'gen_time_table', 'Time Table Lines',
                                              domain=[('day', '=', '7')], required=True),
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
    }

    def gen_datewise(self, cr, uid, line, st_date, en_date, self_obj, context={}):
        time_pool = self.pool.get('op.timetable')
        day_cnt = 7
        curr_date = st_date
        while curr_date <= en_date:
            hour = line.period_id.hour
            if line.period_id.am_pm == 'pm' and int(hour) != 12:
                hour = int(hour)+12
            per_time = '%s:%s:00' % (hour, line.period_id.minute)
            dt_st = utils.server_to_local_timestamp(curr_date.strftime("%Y-%m-%d ") + per_time, "%Y-%m-%d %H:%M:%S",
                                                    "%Y-%m-%d %H:%M:%S",
                                                    'GMT',
                                                    server_tz=context.get('tz', 'GMT'),
                                                    )

            curr_date = datetime.datetime.strptime(dt_st, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.timedelta(hours=line.period_id.duration)
            cu_en_date = curr_date + end_time
            a = time_pool.create(cr, uid, {
                'lecturer_id': line.lecturer_id.id,
                'subject_id': line.subject_id.id,
                'standard_id': self_obj.standard_id.id,
                'period_id': line.period_id.id,
                'start_datetime': curr_date.strftime("%Y-%m-%d %H:%M:%S"),
                'end_datetime': cu_en_date.strftime("%Y-%m-%d %H:%M:%S"),
                'type': curr_date.strftime('%A'),
                'classroom_id': self_obj.classroom_id.id, })

            curr_date = curr_date+datetime.timedelta(days=day_cnt)

        return True

    def act_gen_time_table(self, cr, uid, ids, context={}):
        for self_obj in self.browse(cr, uid, ids, context=context):
            st_date = datetime.datetime.strptime(self_obj.start_date,'%Y-%m-%d')
            en_date = datetime.datetime.strptime(self_obj.end_date,'%Y-%m-%d')
            st_day = week_number[st_date.strftime('%a')]
            for line in self_obj.time_table_lines:
                if int(line.day) == st_day:
                    self.gen_datewise(cr, uid, line, st_date, en_date, self_obj, context=context)
                if int(line.day) < st_day:
                    new_st_date = st_date - datetime.timedelta(days=(st_day - int(line.day)))
                    self.gen_datewise(cr, uid, line, new_st_date, en_date, self_obj, context=context)
                if int(line.day) > st_day:
                    new_st_date = st_date + datetime.timedelta(days=(int(line.day) - st_day ))
                    self.gen_datewise(cr, uid, line, new_st_date, en_date, self_obj, context=context)

        return {'type': 'ir.actions.act_window_close'}


    # def _check_startdate(self, cr, uid, dates, context=None):
    #     for obj in self.browse(cr, uid,  dates):
    #         selected_start_date = obj.start_date
    #         current_date = date.today()
    #         if selected_start_date and current_date:
    #             datetime_format = "%Y-%m-%d"
    #             sdate = datetime.strptime(selected_start_date, datetime_format)
    #             tday = datetime.strptime(current_date.strftime('%Y%m%d'), '%Y%m%d')
    #             if sdate < tday:
    #                 return False
    #             else:
    #                 return True
    #
    # _constraints = [
    #     (_check_startdate,'Invalid Starting Date!',['start_date']),
    # ]

    def _check_date(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            start_date = obj.start_date
            end_date = obj.end_date
            if start_date and end_date:
                datetime_format = "%Y-%m-%d"
                from_dt = datetime.datetime.strptime(start_date, datetime_format)
                to_dt = datetime.datetime.strptime(end_date, datetime_format)
                if to_dt < from_dt:
                    return False
                return True

    _constraints = [
        (_check_date, 'End Date should be greater than Start Date!', ['start_date', 'end_date']),
    ]

generate_time_table()


class generate_time_table_line(osv.osv_memory):

    # def onchange_lecturer(self, cr, uid, lecturer_id, context=None):
    #     lecturer = lecturer_id
    #     related_records = self.pool.get('lecturer_subject_rel').browse(cr, uid, [('op_lecturer_id', '=', lecturer)])
    #     related_subjects = related_records.op_subject_id
    #     subject_ids = self.pool.get('op.subject').browse(cr, uid, [('subject_id', '=', related_subjects)])
    #     return{'value': {'subject_id': subject_ids}}

    _name = 'gen.time.table.line'
    _description = 'Generate Time Table Lines'
    _inherits = {'op.lecturer': 'lecturer_subject_ids'}
    _rec_name = 'day'

    _columns = {
        'gen_time_table': fields.many2one('generate.time.table', 'Time Table', required=True),
        'lecturer_id': fields.many2one('op.lecturer', 'Lecturer', required=True),
        'subject_id': fields.many2one('op.subject', 'Subject', required=True),
        'day': fields.selection([('1', 'Monday'),
                                 ('2', 'Tuesday'),
                                 ('3', 'Wednesday'),
                                 ('4', 'Thursday'),
                                 ('5', 'Friday'),
                                 ('6', 'Saturday'),
                                 ('7', 'Sunday'),
                                 ], 'Day', required=True),
        'period_id': fields.many2one('op.period', 'Period',  required=True),
    }

    def onchange_lecturer(self, cr, uid, lecturer_id, context=None):
        lecturer = lecturer_id
        related_records = self.pool.get('lecturer_subject_rel').browse(cr, uid, [('op_lecturer_id', '=', lecturer)])
        related_subjects = related_records.op_subject_id
        subject_ids = self.pool.get('op.subject').browse(cr, uid, [('subject_id', '=', related_subjects)])
        return{'value': {'subject_id': subject_ids}}

generate_time_table_line()
