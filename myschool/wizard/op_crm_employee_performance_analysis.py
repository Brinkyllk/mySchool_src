from openerp.tools.translate import _
from openerp.osv import orm, fields


class op_crm_employee_performance_analysis_xls(orm.TransientModel):
    _name = 'op.crm.employee.performance.analysis.xls'
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'user_id': fields.many2one('res.users', 'SalesPerson'),
    }

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

        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'op.crm.employee.performance.analysis.xls',
                    'datas': params}
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'report.op.crm.employee.performance.analysis.xls'}

