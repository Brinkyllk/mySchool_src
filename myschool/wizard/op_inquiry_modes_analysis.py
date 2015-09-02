from openerp.tools.translate import _
from openerp.osv import orm, fields


class op_inquiry_modes_analysis_xls(orm.TransientModel):
    _name = 'op.inquiry.modes.analysis.xls'
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'modes_of_inquiry': fields.many2one('op.lead.modes', 'Mode of Inquiry'),
    }

    def xls_export(self, cr, uid, ids, context=None):
        return self.print_report(cr, uid, ids, context=context)

    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        data = self.browse(cr, uid, ids)[0]

        params = {'modes_of_inquiry': 0,'start_date': False, 'end_date': False}
        params['modes_of_inquiry_name'] = data.modes_of_inquiry.name
        params['modes_of_inquiry_id'] = data.modes_of_inquiry.id
        params['start_date'] = data.start_date
        params['end_date'] = data.end_date

        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'op.inquiry.modes.analysis.xls',
                    'datas': params}
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'report.op.inquiry.modes.analysis.xls'}