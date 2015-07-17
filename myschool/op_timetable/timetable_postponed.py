from openerp.osv import osv, fields
import dateutil
from .. import utils
from dateutil import parser
import datetime
import calendar


class timetable_postponed(osv.osv_memory):
    _name = 'timetable.postponed'
    _columns = {
        'period_id': fields.many2one('op.period', 'Period', required=True),
        'classroom_id': fields.many2one('op.classroom', 'Classroom', required=True),
        'date': fields.date('Date', required=True),
    }

    #..get the currect active id of the record..#
    def default_get(self, cr, uid, fields, context=None):
        data = super(timetable_postponed, self).default_get(cr, uid, fields, context=context)
        global timetable_map
        timetable_map = context.get('active_id')
        return data

    #...............Lecturer room conflict..................#
    def _lecturer_conflict(self, cr, uid, ids, context=None):
        self_object = self.browse(cr, uid, ids, context=None)
        lec_id_info = self.pool.get('op.timetable').read(cr, uid, timetable_map, ['lecturer_id'])
        lec_id = lec_id_info.get('lecturer_id')
        lec_id_new = lec_id[0]
        a = self_object.period_id.id
        b = self_object.classroom_id.id
        c = self_object.date
        st_date = dateutil.parser.parse(c).date()
        day = calendar.day_name[st_date.weekday()]
        period_info = self.pool.get('op.period').read(cr, uid, a, ['start_time', 'end_time'])
        per_start = period_info.get('start_time')
        per_end = period_info.get('end_time')
        obj = self.pool.get("op.timetable").search(cr, uid, [('lecturer_id', '=', lec_id_new)])
        print obj
        if obj:
            res = {}
            for record_id in obj:
                for rec_id in obj:
                    details = self.pool.get('op.timetable').read(cr, uid, rec_id,
                                                                 ['type', 'start_datetime', 'period_id'])
                    period_get = details.get('period_id')
                    period_get_id = period_get[0]
                    period_info = self.pool.get('op.period').read(cr, uid, period_get_id, ['start_time', 'end_time'])
                    period_info_start = period_info.get('start_time')
                    period_info_end = period_info.get('end_time')
                    day_type = str(details.get('type'))
                    if day_type == day:
                        asn_date = dateutil.parser.parse(details.get('start_datetime')).date()
                        if st_date <= asn_date:
                            if per_start <= period_info_start < per_end or per_start < period_info_end < per_end:
                                return False
        else:
            return True
        return True

    #...............Class room conflict..................#
    def _classroom_conflict(self, cr, uid, ids, context=None):
        #.. capture the input values ..#
        self_object = self.browse(cr, uid, ids, context=None)
        classroom_id = self_object.classroom_id.id
        period_id = self_object.period_id.id
        date_info = self_object.date

        #.. getting the day of th date..#
        st_date = dateutil.parser.parse(date_info).date()
        day = calendar.day_name[st_date.weekday()]

        #..getting the start and end times of the period..#
        period_info = self.pool.get('op.period').read(cr, uid, period_id, ['start_time', 'end_time'])
        per_start = period_info.get('start_time')
        per_end = period_info.get('end_time')

        #..Capture the ids that contain same classroom id..#
        obj = self.pool.get("op.timetable").search(cr, uid, [('classroom_id', '=', classroom_id)])
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
                    if st_date <= asn_date:
                        if per_start <= period_info_start < per_end or per_start < period_info_end < per_end:
                            return False

            else:
                return True
        return True

    #.................Standard Conflict....................#
    def _standard_conflict(self, cr, uid, ids, context=None):
        #.. Capture standard id ..#
        standard_id_info = self.pool.get('op.timetable').read(cr, uid, timetable_map, ['standard_id'])
        standard_id = standard_id_info.get('standard_id')
        standard_id_new = standard_id[0]

        #.. capture the input values ..#
        self_object = self.browse(cr, uid, ids, context=None)
        classroom_id = self_object.classroom_id.id
        period_id = self_object.period_id.id
        date_info = self_object.date

        #.. getting the day of th date..#
        st_date = dateutil.parser.parse(date_info).date()
        day = calendar.day_name[st_date.weekday()]

        #..getting the start and end times of the period..#
        period_info = self.pool.get('op.period').read(cr, uid, period_id, ['start_time', 'end_time'])
        per_start = period_info.get('start_time')
        per_end = period_info.get('end_time')

        #..Cpature the ids that contain same standard ir..#
        obj = self.pool.get('op.timetable').search(cr, uid, [('standard_id', '=', standard_id_new), ], order=None)
        if obj:
            for record_id in obj:
                details = self.pool.get('op.timetable').read(cr, uid, record_id,
                                                             ['type', 'start_datetime', 'period_id'])
                period_get = details.get('period_id')
                period_get_id = period_get[0]
                period_info = self.pool.get('op.period').read(cr, uid, period_get_id, ['start_time', 'end_time'])
                period_info_start = period_info.get('start_time')
                period_info_end = period_info.get('end_time')
                day_type = str(details.get('type'))
                if day_type == day:
                    asn_date = dateutil.parser.parse(details.get('start_datetime')).date()
                    if st_date <= asn_date:
                        if per_start <= period_info_start < per_end or per_start < period_info_end < per_end:
                            return False

        else:
            return True
        return True

    #.. Validate to can't add back date records..#
    def _validate_backdate(self, cr, uid, ids, context=None):
        now = datetime.datetime.today()
        today = now.strftime('%Y-%m-%d')
        date_today = dateutil.parser.parse(today).date()
        self_object = self.browse(cr, uid, ids, context=context)
        star_datetime = self_object.date
        obj_st_date = dateutil.parser.parse(star_datetime).date()
        if date_today > obj_st_date:
            return False
        else:
            return True

    #..Update the values at postponed..#
    def get_data(self, cr, uid, ids, context=None):
        print timetable_map
        a = self.pool.get('op.timetable')
        for new_obj in self.browse(cr, uid, ids, context=context):
            new_period = new_obj.period_id.id
            b = self.pool.get('op.period').read(cr, uid, new_period, ['hour', 'minute', 'am_pm', 'end_time'])
            c = str(b.get('end_time'))
            d = c.split(".", 1)
            e = str(d[0])
            f = str(d[1])
            g = float('0' + '.' + f)
            h = int(g * 60)
            i = str(h)
            end_time = str(e + ':' + i + ':' + '00')
            am_pm = b.get('am_pm')
            hours = int(b.get('hour'))
            if am_pm == 'pm':
                if hours == 12:
                    pass
                else:
                    hours += 12
            hrs = str(hours)
            minutes = b.get('minute')
            start_time = str(hrs + ':' + minutes + ':' + '00')
            new_classroom = new_obj.classroom_id.id
            new_date = new_obj.date
            start_datetime_new = new_date + ' ' + start_time
            start_datetime_new = datetime.datetime.strptime(start_datetime_new, "%Y-%m-%d %H:%M:%S")
            end_datetime_new = new_date + ' ' + end_time
            end_datetime_new = datetime.datetime.strptime(end_datetime_new, "%Y-%m-%d %H:%M:%S")
            # new_st_date = datetime.datetime.strptime(start_datetime_new, "%Y-%m-%d %H:%M:%S")
            new_st_date = utils.server_to_local_timestamp(start_datetime_new.strftime("%Y-%m-%d ") + start_time, "%Y-%m-%d %H:%M:%S",
                                                    "%Y-%m-%d %H:%M:%S",
                                                    'GMT',
                                                    server_tz=context.get('tz', 'GMT'),
                                                    )
            # new_en_date = datetime.datetime.strptime(end_datetime_new, "%Y-%m-%d %H:%M:%S")
            new_en_date = utils.server_to_local_timestamp(end_datetime_new.strftime("%Y-%m-%d ") + end_time, "%Y-%m-%d %H:%M:%S",
                                                    "%Y-%m-%d %H:%M:%S",
                                                    'GMT',
                                                    server_tz=context.get('tz', 'GMT'),
                                                    )
            day = calendar.day_name[start_datetime_new.weekday()]

            a.write(cr, uid, [timetable_map], {'period_id': new_period, 'start_datetime': new_st_date,
                                               'end_datetime': new_en_date, 'classroom_id': new_classroom, 'type': day,
                                               'state': 'postponed'})

        return True

    _constraints = [
        # (_lecturer_conflict, 'Lecturer not available!!', ['period_id', 'classroom_id', 'date']),
        # (_classroom_conflict, 'Classroom not available', ['classroom_id', 'period_id', 'date']),
        # (_standard_conflict, 'Standard not available', ['classroom_id', 'date', 'period_id']),
        (_validate_backdate, 'You cannot backdate records!', ['start_datetime']),
    ]

