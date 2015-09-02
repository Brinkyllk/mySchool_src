from openerp.tools.translate import _
from openerp.osv import orm, fields
import datetime

# ..generate..#
class op_followup_actions_detail_analysis_xls(orm.TransientModel):
    _name = 'op.followup.actions.detail.analysis.xls'
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'study_programme_id': fields.many2one('op.study.programme', 'Study Programme'),
    }

    #Check Backdate validation for planned start date and end date
    def _check_filter_date(self, cr, uid, vals, context=None):
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
            else:
                return True

    _constraints = [
        (_check_filter_date, 'End Date should be greater than Start Date!', ['start_date', 'end_date'])
    ]

    def xls_export(self, cr, uid, ids, context=None):
        return self.print_report(cr, uid, ids, context=context)

    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        data = self.browse(cr, uid, ids)[0]

        params = {'study_programme_id': 0, 'start_date': False, 'end_date': False}
        params['study_programme_name'] = data.study_programme_id.name
        params['study_programme_id'] = data.study_programme_id.id
        params['start_date'] = data.start_date
        params['end_date'] = data.end_date

        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'op.followup.actions.detail.analysis.xls',
                    'datas': params}
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'report.op.followup.actions.detail.analysis.xls'}