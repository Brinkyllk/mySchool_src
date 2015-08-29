from openerp.tools.translate import _
from openerp.osv import orm, fields


class op_crm_lead_analysis_xls(orm.TransientModel):
    _name = 'op.crm.lead.analysis.xls'
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'study_programme_id': fields.many2one('op.study.programme', 'Study Programme'),
    }

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
                    'report_name': 'op.crm.lead.analysis.xls',
                    'datas': params}
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'report.op.crm.lead.analysis.xls'}

