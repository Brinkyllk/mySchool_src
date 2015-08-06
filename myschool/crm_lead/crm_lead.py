from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import api
import re


class crm_tags(osv.Model):
    _name = "crm.tags"
    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Name', required=True)
    }


class modes(osv.Model):
    _name = 'modes'
    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Name', required=True)
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
        'source_id': fields.many2many('crm.tracking.source', 'campaign_source_rel', 'campaign_id', 'source_id',
                                      'Source(s)'),
    }


class crm_tracking_source(osv.Model):
    _inherit = 'crm.tracking.source'
    _description = "adding fields to crm.lead"
    _columns = {
        'channel_id': fields.many2one('crm.tracking.medium', 'Channel'),
    }


class follow_up_type(osv.Model):
    _name = 'follow.up.type'
    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Name', required=True)
    }


class crm_lead(osv.Model):

    #onchange for prospective_student limit
    @api.onchange('prospective_student')
    def onchange_pstudent(self, cr, uid, ids, prospective_student):
        if prospective_student > 999:
            raise osv.except_osv('Prospective Students', 'Limit exceeded !')
        else:
            return True

    #onchange for is_new course
    @api.multi
    def onchange_new_course(self, is_new_course):
        if is_new_course:
            return True

    _inherit = 'crm.lead'
    _rec_name = 'name'
    _description = "adding fields to crm.lead"


    def _meeting_count(self, cr, uid, ids, field_name, arg, context=None):
        Event = self.pool['calendar.event']
        return {
            opp_id: Event.search_count(cr,uid, [('opportunity_id', '=', opp_id)], context=context)
            for opp_id in ids
        }


    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='set null', track_visibility='onchange',
            select=True, help="Linked student (optional). Usually created when converting the lead.", domain="[('is_student', '=', True)]"),
        'modes': fields.many2one('modes','Modes of Inquiries'),
        'courses_interested': fields.many2many('op.study.programme', 'study_programme_lead_rel', 'crm_id', 'name',
                                               'Study programme(s) Interested'),
        'anytime': fields.many2many('time.frame', 'anytime_time_frame', 'anytime', 'name', 'Anytime'),
        'morning': fields.many2many('time.frame', 'morning_time_frame', 'morning', 'name', 'Morning'),
        'afternoon': fields.many2many('time.frame', 'afternoon_time_frame', 'afternoon', 'name', 'Afternoon'),
        'evening': fields.many2many('time.frame', 'evening_time_frame', 'evening', 'name', 'Evening'),
        'prospective_student': fields.integer(size=5, string='# Prospective Students'),
        'inquiry_date': fields.date(string='Inquiry Date'),
        'tags': fields.many2many('crm.tags', 'crm_lead_tags_rel', id1='partner_id', id2='code', string='Tags'),
        'is_new_course': fields.boolean('New Course', help="Check if the course is not exist"),
        'meeting_count': fields.function(_meeting_count, string='# Meetings', type='integer', store=True),
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

        #open student profile or registrtion form
        crmRef = self.pool.get('crm.lead')
        resPartnerRef = self.pool.get('res.partner')
        studentRef = self.pool.get('op.student')

        crmId = crmRef.browse(cr, uid, ids, context=context)
        partnerId = crmRef.browse(cr, uid, crmId.partner_id.id, context=context)
        newPartner_id = partnerId.id

        isStudent = resPartnerRef.read(cr, uid, newPartner_id, ['is_student'])
        if isStudent:
            newIsStudent = isStudent.get('is_student')

            if newIsStudent != False:
                newStudent_id = studentRef.search(cr, uid, [('partner_id', '=', newPartner_id)])
                student = newStudent_id[0]

            models_data = self.pool.get('ir.model.data')
            form_view = models_data.get_object_reference(cr, uid, 'myschool', 'view_op_enrollment_form')
            tree_view = models_data.get_object_reference(cr, uid, 'myschool', 'view_op_enrollment_tree')

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
                    'res_model': 'op.enrollment',
                    'view_id': 'False',
                    'views': [(form_view and form_view[1] or False, 'form'),
                              (tree_view and tree_view[1] or False, 'tree')],
                    'type': 'ir.actions.act_window',
                    'flags': {'action_buttons': True},
                    'target': 'new',
                    'nodestroy': True
                }
            return value
        else:
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
        return True

    # email validation........
    def validate_email(self, cr, uid, ids, email_from):
        email_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")
        valid_email = False
        if email_from is False:
            return True
        if email_re.match(email_from):
            valid_email=True
            return True
        else:
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid Email'))

    def create(self, cr, uid, vals, context=None):

        # email validation on create
        if 'email_from' in vals:
            self.validate_email(cr, uid, [], vals['email_from'])

        # prospective_student validation on create
        if 'prospective_student' in vals:
            self.onchange_pstudent(cr, uid, [], vals['prospective_student'])

            return super(crm_lead, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, values, context=None):

        # email validation on write
        if 'email_from' in values:
            self.validate_email(cr, uid, ids, values['email_from'])

        # prospective_student validation on write
        if 'prospective_student' in values:
            self.onchange_pstudent(cr, uid, ids, values['prospective_student'])

        return super(crm_lead, self).write(cr, uid, ids, values, context=context)


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


class calendar_event(osv.Model):
    _inherit = 'calendar.event'
    _columns = {
        'type': fields.many2one('follow.up.type', 'Follow-up Type')
    }

    def default_get(self, cr, uid, fields, context=None):
        data = super(calendar_event, self).default_get(cr, uid, fields, context=context)
        activeId = context.get('active_id')
        if activeId:
            data['opportunity_id'] = activeId
        return data
calendar_event()


class follow_up_type(osv.Model):
    _name = 'follow.up.type'
    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Name', required=True)
    }
