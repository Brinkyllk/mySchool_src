from openerp.osv import osv, fields
from openerp.tools.translate import _


class crm_lead(osv.Model):
    _inherit = 'crm.lead'
    _description = "adding fields to crm.lead"
    _columns = {
        'courses_interested': fields.many2many('op.course', 'course_crm_lead_rel', 'crm_id', 'name',
                                               'Course(s) Interested'),
        'weekday': fields.many2many('time.frame', 'weekday_time_frame', 'weekday', 'name', 'Weekday'),
        'saturday': fields.many2many('time.frame', 'saturday_time_frame', 'saturday', 'name', 'Saturday'),
        'sunday': fields.many2many('time.frame', 'sunday_time_frame', 'sunday', 'name', 'Sunday'),
        'prospective_student': fields.integer(size=5, string='# Prospective Students'),
        'inquiry_date': fields.date(string='Inquiry Date'),
    }

    def case_mark_won(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100
        """
        stages_leads = {}
        for lead in self.browse(cr, uid, ids, context=context):
            stage_id = self.stage_find(cr, uid, [lead], lead.section_id.id or False,
                                       [('probability', '=', 100.0), ('fold', '=', True)], context=context)
            if stage_id:
                if stages_leads.get(stage_id):
                    stages_leads[stage_id].append(lead.id)
                else:
                    stages_leads[stage_id] = [lead.id]
            else:
                raise osv.except_osv(_('Warning!'),
                                     _(
                                         'To relieve your sales pipe and group all Won opportunities, configure one of your sales stage as follow:\n'
                                         'probability = 100 % and select "Change Probability Automatically".\n'
                                         'Create a specific stage or edit an existing one by editing columns of your opportunity pipe.'))
        for stage_id, lead_ids in stages_leads.items():
            self.write(cr, uid, lead_ids, {'stage_id': stage_id}, context=context)

        #open student profile
        crmRef = self.pool.get('crm.lead')
        resPartnerRef = self.pool.get('res.partner')
        studentRef = self.pool.get('op.student')

        crmId = crmRef.browse(cr, uid, ids, context=context)[0]
        partnerId = crmRef.browse(cr, uid, crmId.partner_id.id, context=context)[0]
        newPartner_id = partnerId.id

        isStudent = resPartnerRef.read(cr, uid, newPartner_id, ['is_student'])
        newIsStudent = isStudent.get('is_student')

        newStudent_id = studentRef.search(cr, uid, [('partner_id', '=', newPartner_id)])
        domain = [('id', '=', newStudent_id)]

        if newIsStudent == False:
            value = {
                'name': 'Student',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'op.student',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
            }
            return value
        else:
            value = {
                'name': 'Student',
                'view_mode': 'tree',
                'view_type': 'tree',
                'res_model': 'op.student',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'domain': domain,
            }
            return value
        return True


class time_frame(osv.Model):
    _name = 'time.frame'
    _columns = {
        'name': fields.char('Time Frame')
    }


class crm_tracking_campaign(osv.Model):
    _inherit = 'crm.tracking.campaign'
    _description = "adding fields to crm.lead"
    _columns = {
        'source_id': fields.many2many('crm.tracking.source', 'campaign_source_rel', 'campaign_id', 'source_id',
                                      'Source(s)'),
    }


class crm_tracking_source(osv.Model):
    _inherit = 'crm.tracking.source'
    _description = "adding fields to crm.lead"
    _columns = {
        'channel_id': fields.many2one('crm.tracking.medium', 'Channel'),
    }

