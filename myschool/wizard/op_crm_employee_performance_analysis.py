from openerp.tools.translate import _
from openerp.osv import orm, fields
import datetime


class op_crm_employee_performance_analysis_xls(orm.TransientModel):
    _name = 'op.crm.employee.performance.analysis.xls'
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'user_id': fields.many2one('res.users', 'SalesPerson'),
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

        params = {'user_id': False, 'start_date': False, 'end_date': False}
        params['user_name'] = data.user_id.partner_id.name
        params['user_id'] = data.user_id.id
        params['start_date'] = data.start_date
        params['end_date'] = data.end_date
        partner_id = self.pool.get('res.users').read(cr, uid, uid, ['partner_id'])
        params['uname'] = partner_id.get('partner_id')[1]

        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'op.crm.employee.performance.analysis.xls',
                    'datas': params}
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'report.op.crm.employee.performance.analysis.xls'}

