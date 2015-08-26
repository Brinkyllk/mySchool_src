from openerp.osv import osv,fields
from openerp.tools.translate import _
import datetime
import time


class op_crm_lead_analysis(osv.osv_memory):
    _name = 'op.crm.lead.analysis'
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'study_programme_id': fields.many2one('op.study.programme', 'Study Programme'),
    }

    # def gen_time_table_report(self, cr, uid, ids, context={}):
    #     value = {}
    #     data = self.read(cr, uid, ids, ['start_date', 'end_date', 'study_programme_id'], context=context)
    #
    #     if data[0]['study_programme_id']:
    #         time_table_ids = self.pool.get('op.crm.lead.analysis.report').search(
    #             cr, uid,
    #             [('id', '=', data[0]['study_programme_id'][0]),
    #              ('start_datetime', '>', data[0]['start_date'] + '%H:%M:%S'),
    #              ('end_datetime', '<', data[0]['end_date'] + '%H:%M:%S'),
    #              ])
    #
    #         data[0].update({'time_table_ids': time_table_ids})
    #     else:
    #         teacher_time_table_ids = self.pool.get('op.timetable').search(
    #             cr, uid,
    #             [('start_datetime', '>', data[0]['start_date'] + '%H:%M:%S'),
    #              ('end_datetime', '<', data[0]['end_date'] + '%H:%M:%S'),
    #              ])
    #
    #         data[0].update({'teacher_time_table_ids': teacher_time_table_ids})

    def gen_lead_analysis(self, cr, uid, ids, context={}):
        return self.pool['report'].get_action(cr, uid, [], 'myschool.op_crm_lead_analysis_report_generate',
                                              context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

