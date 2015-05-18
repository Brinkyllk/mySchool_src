from openerp.osv import osv, fields
import dateutil
from dateutil import  parser
import datetime
import  calendar


class timetable_postponed(osv.osv_memory):
    _name = 'timetable.postponed'
    _columns = {
        'timetable_id': fields.many2one('op.period'),
        'period_id': fields.many2one('op.period', 'Period'),
        'classroom_id': fields.many2one('op.classroom', 'Classroom'),
        'date': fields.date('Date'),
    }


    def default_get(self, cr, uid, fields, context=None):

        data = super(timetable_postponed, self).default_get(cr, uid, fields, context=context)
        global  timetable_map
        timetable_map = context.get('active_id')
        return data


    def get_data(self, cr, uid, ids, context=None):
        print timetable_map
        a= self.pool.get('op.timetable')
        for new_obj in self.browse(cr, uid, ids, context=context):
            new_period = new_obj.period_id.id
            b = self.pool.get('op.period').read(cr, uid, new_period, ['hour', 'minute', 'am_pm', 'end_time'])
            c = str(b.get('end_time'))
            d = c.split(".", 1)
            e = str(d[0])
            f = str(d[1])
            g = float('0'+'.'+f)
            h = int(g*60)
            i = str(h)
            end_time = str(e+':'+i+':'+'00')
            am_pm = b.get('am_pm')
            hours = int(b.get('hour'))
            if am_pm == 'pm':
                if hours == 12:
                    pass
                else:
                    hours += 12
            hrs = str(hours)
            minutes = b.get('minute')
            start_time = str(hrs+':'+minutes+':'+'00')
            new_classroom = new_obj.classroom_id.id
            new_date = new_obj.date
            start_datetime_new = new_date+' '+start_time
            end_datetime_new = new_date+' '+end_time
            new_st_date = datetime.datetime.strptime(start_datetime_new, "%Y-%m-%d %H:%M:%S")
            new_en_date = datetime.datetime.strptime(end_datetime_new, "%Y-%m-%d %H:%M:%S")
            day = calendar.day_name[new_st_date.weekday()]

            a.write(cr, uid, [timetable_map], {'period_id': new_period, 'start_datetime': new_st_date,
                                               'end_datetime': new_en_date, 'classroom_id': new_classroom, 'type':day, 'state':'postponed'})


        return True
