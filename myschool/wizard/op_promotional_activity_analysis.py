from openerp.tools.translate import _
from openerp.osv import orm, fields


class op_promotional_activity_analysis_xls(orm.TransientModel):
    _name = 'op.promotional.activity.analysis.xls'
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'study_programme_id': fields.many2one('op.study.programme', 'Study Programme'),
    }