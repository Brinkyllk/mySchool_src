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

    '''==========When the opportunity won the student is already in the system load the student form with the details
                else load the load the registration form============'''
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
        student = newStudent_id[0]

        models_data = self.pool.get('ir.model.data')
        form_view = models_data.get_object_reference(cr, uid, 'myschool', 'view_student_form')
        tree_view = models_data.get_object_reference(cr, uid, 'myschool', 'view_student_tree')

        if newIsStudent == False:
            value = {
                'name': 'Student',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'op.registration',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
            }
            return value
        else:

            value = {
                'domain': str([('id', '=', newStudent_id)]),
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'op.student',
                'view_id': False,
                'views': [(form_view and form_view[1] or False, 'form'),
                          (tree_view and tree_view[1] or False, 'tree')],
                'type': 'ir.actions.act_window',
                'res_id': student,
                'target': 'current',
                'nodestroy': True
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

# class crm_partner_binding(osv.osv_memory):
#     _inherit = 'crm.partner.binding'
#     _description = "editing fields in convert to opportunities"
#     _columns ={
#         'action': fields.selection([
#                 ('exist', 'Link to an existing customer'),
#                 ('create', 'Create a new customer'),
#                 ('nothing', 'Do not link to a customer')
#             ], 'Related Customer', required=True),
#     }

# class crm_lead2opportunity_partner(osv.osv_memory):
#     _name = 'crm.lead2opportunity.partner'
#     _description = 'Lead To Opportunity Partner'
#     _inherit = 'crm.partner.binding'
#
#     _columns = {
#         'name': fields.selection([
#                 ('convert', 'Convert to opportunity'),
#                 ('merge', 'Merge with existing opportunities')
#             ], 'Conversion Action', required=True),
#         'opportunity_ids': fields.many2many('crm.lead', string='Opportunities'),
#         'user_id': fields.many2one('res.users', 'Salesperson', select=True),
#         'section_id': fields.many2one('crm.case.section', 'Sales Team', select=True),
#     }

# class crm_lead2opportunity_mass_convert(osv.osv_memory):
#     _name = 'crm.lead2opportunity.partner.mass'
#     _description = 'Mass Lead To Opportunity Partner'
#     _inherit = 'crm.lead2opportunity.partner'
#
#     _columns = {
#         # 'user_ids':  fields.many2many('res.users', string='Salesmen'),
#         # 'section_id': fields.many2one('crm.case.section', 'Sales Team'),
#         # 'deduplicate': fields.boolean('Apply deduplication', help='Merge with existing leads/opportunities of each partner'),
#         'action': fields.selection([
#                 ('each_exist_or_create', 'Use existing partner or create'),
#                 ('nothing', 'Do not link to a customer')
#             ], 'Related Customer', required=True),
#         # 'force_assignation': fields.boolean('Force assignation', help='If unchecked, this will leave the salesman of duplicated opportunities'),
#     }

