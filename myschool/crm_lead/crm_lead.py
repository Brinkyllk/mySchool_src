from openerp.osv import osv, fields

class crm_lead(osv.Model):
    _inherit = 'crm.lead'
    _description = "adding fields to crm.lead"
    _columns = {
        'new_one':fields.char('New One', size=50),
    }
crm_lead()