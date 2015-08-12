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

    # check prospective_student limit
    def _check_pstudent(self, cr, uid, ids, prospective_student):
        if prospective_student > 999:
            raise osv.except_osv('Prospective Students', 'Limit exceeded !')
        else:
            return True

    # ..onchange for is_new course
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
        'modes': fields.many2one('modes','Mode of Inquiry'),
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

        'address_line1': fields.char('address line1', size=20),
        'address_line2': fields.char('address line2', size=25),
        'town': fields.char('town', size=25),
        'province': fields.char('province', size=20),
        'nation': fields.char('nation', size=20),
        'meeting_count': fields.function(_meeting_count, string='# Meetings', type='integer', store=True),

        'first_name': fields.char('First Name', size=30),
        'last_name': fields.char('Last Name', size=30),

    }

    # ------check spaces in address line one----#
    def _check_add_l_one(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.address_line1)
        if not value:
            return False
        else:
            return True

    # ------check spaces in address line two----#
    def _check_add_l_two(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.address_line2)
        if not value:
            return False
        else:
            return True

    # -----check spaces in town-----------------#
    def _check_town(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.town)
        if not value:
            return False
        else:
            return True

    # -----check spaces in province--------------#
    def _check_province(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.province)
        if not value:
            return False
        else:
            return True

    # -----check spaces in country---------------#
    def _check_nation(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.nation)
        new_value = value.replace(" ", "")
        if not new_value or not new_value.isalpha():
            return False
        else:
            return True

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

        # open student profile or registrtion form
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
                'target': 'new',
                }
            return value
        return True

    # phone number validation for customer
    def phoneNumberValidation(self, cr, uid, ids, phoneNumber):
        phone_re = re.compile(ur'^(\+\d{1,1}[- ]?)?\d{10}$|(\+\d{1,1}[- ]?)?\d{9}$')
        valid_phone = False
        if phoneNumber is False:
            return True
        if phone_re.match(phoneNumber):
            valid_phone=True
            return True
        else:
            raise osv.except_osv(_('Invalid Phone Number'), _('Please enter a valid Phone Number'))

    # mobile number validation for customer
    def mobileNumberValidation(self, cr, uid, ids, mobileNumber):
        mobile_re = re.compile(ur'^(\+\d{1,1}[- ]?)?\d{10}$|(\+\d{1,1}[- ]?)?\d{9}$')
        valid_mobile = False
        if mobileNumber is False:
            return True
        if mobile_re.match(mobileNumber):
            valid_mobile=True
            return True
        else:
            raise osv.except_osv(_('Invalid Mobile Number'), _('Please enter a valid Mobile Number'))

    # fax number validation for customer
    def faxNumberValidation(self, cr, uid, ids, faxNumber):
        fax_re = re.compile(ur'^(\+\{1,1}[- ]?)?\d{10}$')
        valid_fax = False
        if faxNumber is False:
            return True
        if fax_re.match(faxNumber):
            valid_fax = True
            return True
        else:
            raise osv.except_osv(_('Invalid Fax Number'), _('Please enter a valid Fax Number'))

    # .... check passing nul values....#
    def _check_invalid_data(self, cr, uid, ids, subjectName):
        n_name = str(subjectName).replace(",", "")
        n_name = n_name.replace(" ", "")
        n_name = ''.join([i for i in n_name if not i.isdigit()])
        if n_name.isalpha() or n_name.isdigit():
            return True
        else:
            raise osv.except_osv(_('Invalid Subject Description'), _('Please insert valid information'))

    # ..email validation....#
    def validate_email(self, cr, uid, ids, email_from):
        email_re = re.compile("^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$")
        if email_from is False:
            return True
        if email_re.match(email_from):
            return True
        else:
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid Email'))

    # ---------Contact first name validation-------------- #
    def first_name_validation(self, cr, uid, ids, first_name):
        f_name = str(first_name).replace(" ", "")
        f_name = ''.join([i for i in f_name if not i.isdigit()])
        if f_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Contact Name'), _('Please enter a correct Contact name'))

    # ---------Contact last name validation-------------- #
    def last_name_validation(self, cr, uid, ids, last_name):
        l_name = str(last_name).replace(" ", "")
        l_name = ''.join([i for i in l_name if not i.isdigit()])
        if l_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Contact Name'), _('Please enter a correct Contact name'))

    def create(self, cr, uid, vals, context=None):

        # ----------contact first name validation------------- #
        if 'first_name' in vals:
            self.first_name_validation(cr, uid, [], vals['first_name'])

        # ----------contact last name validation-------------- #
        if 'last_name' in vals:
            self.last_name_validation(cr, uid, [], vals['last_name'])

        # -----------phone number validation------------------ #
        if 'phone' in vals:
            self.phoneNumberValidation(cr, uid, [], vals['phone'])

        # ---------- mobile number validation----------------- #
        if 'mobile' in vals:
            self.mobileNumberValidation(cr, uid, [], vals['mobile'])

        # --------------fax number validation----------------- #
        if 'fax' in vals:
            self.faxNumberValidation(cr, uid, [], vals['fax'])

        if 'name' in vals:
            self._check_invalid_data(cr, uid, [], vals['name'])

        # ---------------email validation on create------------ #
        if 'email_from' in vals:
            self.validate_email(cr, uid, [], vals['email_from'])

        # ---------prospective_student validation on create---- #
        if 'prospective_student' in vals:
            self._check_pstudent(self, cr, uid, vals['prospective_student'])

        # ----------Address lines and update res.partner------- #
        if 'address_line1' in vals:
            if vals['address_line1'] is False or None:
                pass
            else:
                line1 = vals['address_line1'].strip()
                vals.update({'street': line1, 'address_line1': line1})

        if 'address_line2' in vals:
            if vals['address_line2'] is False or None:
                pass
            else:
                line2 = vals['address_line2'].strip()
                vals.update({'street2': line2, 'address_line2': line2})

        if 'town' in vals:
            if vals['town'] is False or None:
                pass
            else:
                twn = vals['town'].strip()
                vals.update({'city': twn, 'town': twn})

        if 'province' in vals:
            if vals['province'] is False or None:
                pass
            else:
                prvn = vals['province'].strip()
                vals.update({'province': prvn})

        if 'nation' in vals:
            if vals['nation'] is False or None:
                pass
            else:
                cntry = vals['nation'].strip()
                vals.update({'nation': cntry})

        return super(crm_lead, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, values, context=None):

        # ----contact first name validation function call----- #
        if 'first_name' in values:
            self.first_name_validation(cr, uid, [], values['first_name'])

        # -----contact last name validation function call----- #
        if 'last_name' in values:
            self.last_name_validation(cr, uid, [], values['last_name'])

        # -----phone number validation on write function call-- #
        if 'phone' in values:
            self.phoneNumberValidation(cr, uid, [], values['phone'])

        # -----mobile number validation function call---------- #
        if 'mobile' in values:
            self.mobileNumberValidation(cr, uid, [], values['mobile'])

        # -----fax number validation function call------------- #
        if 'fax' in values:
            self.faxNumberValidation(cr, uid, [], values['fax'])

        if 'name' in values:
            self._check_invalid_data(cr, uid, [], values['name'])

        # ------email validation on write---------------------- #
        if 'email_from' in values:
            self.validate_email(cr, uid, ids, values['email_from'])

        # ------prospective_student validation on write-------- #
        if 'prospective_student' in values:
            self._check_pstudent(self, cr, uid, values['prospective_student'])

        if 'address_line1' in values:
            if values['address_line1'] is False or None:
                pass
            else:
                line1 = values['address_line1'].strip()
                values.update({'street': line1, 'address_line1': line1})

        if 'address_line2' in values:
            if values['address_line2'] is False or None:
                pass
            else:
                line2 = values['address_line2'].strip()
                values.update({'street2': line2, 'address_line2': line2})

        if 'town' in values:
            if values['town'] is False or None:
                pass
            else:
                twn = values['town'].strip()
                values.update({'city': twn, 'town': twn})

        if 'province' in values:
            if values['province'] is False or None:
                pass
            else:
                prvn = values['province'].strip()
                values.update({'province': prvn})

        if 'nation' in values:
            if values['nation'] is False or None:
                pass
            else:
                cntry = values['nation'].strip()
                values.update({'nation': cntry})

        return super(crm_lead, self).write(cr, uid, ids, values, context=context)

    _constraints = [
        (_check_add_l_one, 'Entered Invalid Data in Address line1 !!', ['address_line1']),
        (_check_add_l_two, 'Entered Invalid Data in Address line2 !!', ['address_line2']),
        (_check_town, 'Entered Invalid Data in City !!', ['town']),
        (_check_province, 'Entered Invalid Data in Province !!', ['province']),
        (_check_nation, 'Entered Invalid Data in Country !!', ['nation']),
    ]


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
