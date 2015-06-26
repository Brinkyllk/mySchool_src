from openerp.osv import osv, fields

class crm_lead(osv.Model):
    _inherit = 'crm.lead'
    _description = "adding fields to crm.lead"
    _columns = {
        # 'courses_interested':fields.many2many('op.course','name','Course(s) Interested'),
        'courses_interested':fields.many2many('op.course','course_crm_lead_rel','crm_id','name','Course(s) Interested'),
        'weekday':fields.many2many('time.frame', 'weekday_time_frame', 'weekday', 'name', 'Weekday'),
        'saturday':fields.many2many('time.frame', 'saturday_time_frame', 'saturday', 'name', 'Saturday'),
        'sunday':fields.many2many('time.frame', 'sunday_time_frame', 'sunday', 'name', 'Sunday'),
        # 'saturday':fields.many2many(),
        # 'sunday':fields.many2many()
    }

class time_frame(osv.Model):
    _name = 'time.frame'
    _columns = {
        'name': fields.char('Time Frame')
    }

class crm_tracking_campaign(osv.Model):
    _inherit = 'crm.tracking.campaign'
    _description = "adding fields to crm.lead"
    _columns = {
        'source_id':fields.many2many('crm.tracking.source','campaign_source_rel','campaign_id','source_id','Source(s)'),
    }

class crm_tracking_source(osv.Model):
    _inherit = 'crm.tracking.source'
    _description = "adding fields to crm.lead"
    _columns = {
        'channel_id': fields.many2one('crm.tracking.medium', 'Channel'),
    }