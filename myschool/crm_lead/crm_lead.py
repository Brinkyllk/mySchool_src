from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import api
import re
import dateutil
import datetime
from dateutil import parser


class op_course_tags(osv.Model):

    _name = "op.course.tags"
    _columns = {
        'code': fields.char('Code', required=True, size=5),
        'name': fields.char('Name', required=True, size=30)
    }

    _sql_constraints = [('name', 'UNIQUE (name)', 'The Name of the Tags must be unique!')]

    # ----------------Validations----------------------- s#
    # ---------code validation------------- s#
    def code_validation(self, cr, uid, ids, code):
        crm_tag_code = str(code).replace(" ", "")
        crm_tag_new_code = ''.join([i for i in crm_tag_code if not i.isdigit()])
        lengthTagsCode = len(code)
        if lengthTagsCode >= 2 and crm_tag_new_code.isalpha() and crm_tag_code.isdigit():
            return True
        else:
            if lengthTagsCode <= 2:
                raise osv.except_osv(_('Invalid Code !'), _('Minimum data length should be at least 2 characters'))
            else:
                if str(code).isspace():
                    raise osv.except_osv(_('Invalid Code !'), _('Only Spaces not allowed'))
                elif crm_tag_new_code.isalpha() or crm_tag_code.isdigit():
                    return True
                else:
                    raise osv.except_osv(_('Invalid Code !'), _('Please Enter the code correctly'))

    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        tag_name = str(name).replace(" ", "")
        tag_name = ''.join([i for i in tag_name if not i.isdigit()])
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        else:
            pass

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------code validation caller------- s#
        if 'code' in vals:
            self.code_validation(cr, uid, [], vals['code'])

        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        code = vals['code'].strip().upper().replace(" ", "")
        name = vals['name'].strip()
        vals.update({'code': code, 'name': name})

        return super(op_course_tags, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # ----------code validation caller-------- s#
        if 'code' in values:
            self.code_validation(cr, uid, [], values['code'])

        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        # ------ update the values after removing white spaces---- s#
        if 'name' in values:
            name = values['name'].strip()
            values.update({'name': name})
        if 'code' in values:
            code = values['code'].strip().upper().replace(" ", "")
            values.update({'code': code})

        return super(op_course_tags, self).write(cr, uid, ids, values, context=context)

    def unlink(self, cr, uid, vals, context=None):
        #When delete followups update meeting count
        crmLead = self.pool.get('crm.lead')
        for values in vals:
            k = [values]
            cr.execute('SELECT lead_id FROM op_crm_lead_tags_rel ' \
                       'WHERE tag_id = %s ', (k))

            op_crm_lead_tags_rel_id = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            if op_crm_lead_tags_rel_id:
                int_op_crm_lead_tags_rel_id = int(op_crm_lead_tags_rel_id[0].id)
                list_int_op_crm_lead_tags_rel_id = [int_op_crm_lead_tags_rel_id]
                tags = len(list_int_op_crm_lead_tags_rel_id)
            else:
                tags = 0

            if tags == 0:
                return super(op_course_tags, self).unlink(cr, uid, vals, context=context)
            else:
                raise osv.except_osv('You can not delete this record', 'This Tag already referred in another location')

        return super(op_course_tags, self).unlink(cr, uid, vals, context=context)


class op_lead_modes(osv.Model):

    _name = 'op.lead.modes'
    _columns = {
        'code': fields.char('Code', required=True, size=5,),
        'name': fields.char('Name', required=True, size=30)
    }

    _sql_constraints = [('name', 'UNIQUE (name)', 'The Name of the Mode must be unique!')]

    # ----------------Validations----------------------- s#
    # ---------code validation------------- s#
    def code_validation(self, cr, uid, ids, code):
        modes_code = str(code).replace(" ", "")
        new_modes_code = ''.join([i for i in modes_code if not i.isdigit()])
        lengthModesCode = len(code)
        if lengthModesCode >= 2 and str(modes_code).isalpha():
            return True
        else:
            if lengthModesCode <= 2:
                raise osv.except_osv(_('Invalid Code !'), _('Minimum data length should be at least 2 characters'))
            else:
                if str(code).isspace():
                    raise osv.except_osv(_('Invalid Code !'), _('Only Spaces not allowed'))
                elif new_modes_code.isalpha() or modes_code.isdigit():
                    return True
                else:
                    raise osv.except_osv(_('Invalid Code !'), _('Please Enter the code correctly'))

    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        mode_name = str(name).replace(" ", "")
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        elif mode_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Name !'), _('Please Enter a valid name'))

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------code validation caller------- s#
        if 'code' in vals:
            self.code_validation(cr, uid, [], vals['code'])

        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        code = vals['code'].strip().upper().replace(" ", "")
        name = vals['name'].strip().title()
        vals.update({'code': code, 'name': name})

        return super(op_lead_modes, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # ----------code validation caller-------- s#
        if 'code' in values:
            self.code_validation(cr, uid, [], values['code'])

        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        # ------ update the values after removing white spaces---- s#
        if 'name' in values:
            name = values['name'].strip().title()
            values.update({'name': name})
        if 'code' in values:
            code = values['code'].strip().upper().replace(" ", "")
            values.update({'code': code})

        return super(op_lead_modes, self).write(cr, uid, ids, values, context=context)

    def unlink(self, cr, uid, vals, context=None):
        #When delete followups update meeting count
        crmLead = self.pool.get('crm.lead')
        for values in vals:
            k = [values]
            cr.execute('SELECT id FROM crm_lead ' \
                        'WHERE modes = %s ', (k))

            crm_lead_id = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            if crm_lead_id:
                int_crm_lead_id = int(crm_lead_id[0].id)
                list_int_crm_lead_id = [int_crm_lead_id]
                tags = len(list_int_crm_lead_id)
            else:
                tags = 0

            if tags == 0:
                return super(op_lead_modes, self).unlink(cr, uid, vals, context=context)
            else:
                raise osv.except_osv('You can not delete this record', 'This Mode already referred in another location')

        return super(op_lead_modes, self).unlink(cr, uid, vals, context=context)


class calendar_alarm(osv.Model):
    _inherit = 'calendar.alarm'

    # ------------------Validations----------------------- s#
    # ------------name validation--------------- s#
    def name_validation(self, cr, uid, ids, name):
        dup_name_check = str(name).lower()
        name_val = str(name).replace(" ", "")
        new_name_val = ''.join([i for i in name_val if not i.isdigit()])
        dup_val = self.pool.get("calendar.alarm").search(cr, uid, [('name', '=', dup_name_check)])
        if str(name).isspace():
            raise osv.except_osv(_('Name Field..'), _('Only Spaces not allowed..!'))
        elif len(dup_val) > 0:
            raise osv.except_osv(_('Data Duplication..!'), _('Name value already exists'))
        elif not new_name_val.isalpha():
            raise osv.except_osv(_('Name Field..'), _('Special Characters not allowed'))
        else:
            pass

    # ----------- amount validation----------- s#
    def duration_validation(self, cr, uid, ids, duration):
        new_duration = str(duration).replace(" ", "")
        if duration == 0:
            raise osv.except_osv(_('Amount Field'), _('Amount Field cannot be Null..!'))
        elif len(new_duration) < 3:
            pass
        else:
            raise osv.except_osv(_('Amount Field'), _('Amount limit exceeded.Maximum 2 Digits'))

    # ---------override create function---------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        # ---------duration validation caller------ s#
        if 'duration' in vals:
            self.duration_validation(cr, uid, [], vals['duration'])

        # --------remove useless white spaces------ s#
        name = vals['name'].strip().lower()
        vals.update({'name': name})

        return super(calendar_alarm, self).create(cr, uid, vals, context=context)


class op_time_frame(osv.Model):

    _name = 'op.time.frame'
    _columns = {
        'name': fields.char('Time Frame', size=30, ondelete='no action', required=True)
    }

    _sql_constraints = [('name', 'UNIQUE (name)', 'The Name of the Time Frame must be unique!')]

    # ----------------Validations----------------------- s#
    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        follow_up_type_name = str(name).replace(" ", "")
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        elif follow_up_type_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Name !'), _('Please Enter a valid name'))

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        name = vals['name'].strip().title()
        vals.update({'name': name})

        return super(op_time_frame, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        # ------ update the values after removing white spaces---- s#
        if 'name' in values:
            name = values['name'].strip().title()
            values.update({'name': name})

        return super(op_time_frame, self).write(cr, uid, ids, values, context=context)

    def unlink(self, cr, uid, vals, context=None):
        #When delete followups update meeting count
        crmLead = self.pool.get('crm.lead')
        for values in vals:
            k = [values]
            cr.execute('SELECT lead_id FROM op_anytime_time_frame_rel ' \
                       'WHERE time_frame_id = %s ', (k))

            op_anytime_time_frame_rel_id = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            if op_anytime_time_frame_rel_id:
                int_op_anytime_time_frame_rel_id = int(op_anytime_time_frame_rel_id[0].id)
                list_int_op_anytime_time_frame_rel_id = [int_op_anytime_time_frame_rel_id]
                anyTime = len(list_int_op_anytime_time_frame_rel_id)
            else:
                anyTime = 0

            cr.execute('SELECT lead_id FROM op_afternoon_time_frame_rel ' \
                       'WHERE time_frame_id = %s ', (k))

            op_afternoon_time_frame_rel_id = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            if op_afternoon_time_frame_rel_id:
                int_op_afternoon_time_frame_rel_id = int(op_afternoon_time_frame_rel_id[0].id)
                list_int_op_afternoon_time_frame_rel_id = [int_op_afternoon_time_frame_rel_id]
                afternoon = len(list_int_op_afternoon_time_frame_rel_id)
            else:
                afternoon = 0

            cr.execute('SELECT lead_id FROM op_evening_time_frame_rel ' \
                       'WHERE time_frame_id = %s ', (k))

            op_evening_time_frame_rel_id = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            if op_evening_time_frame_rel_id:
                int_op_evening_time_frame_rel_id = int(op_evening_time_frame_rel_id[0].id)
                list_int_op_evening_time_frame_rel_id = [int_op_evening_time_frame_rel_id]
                evening = len(list_int_op_evening_time_frame_rel_id)
            else:
                evening = 0

            cr.execute('SELECT lead_id FROM op_morning_time_frame_rel ' \
                       'WHERE time_frame_id = %s ', (k))

            op_morning_time_frame_rel_id = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            if op_morning_time_frame_rel_id:
                int_op_morning_time_frame_rel_id = int(op_morning_time_frame_rel_id[0].id)
                list_int_op_morning_time_frame_rel_id = [int_op_morning_time_frame_rel_id]
                morning = len(list_int_op_morning_time_frame_rel_id)
            else:
                morning = 0

            if morning == 0 and anyTime == 0 and afternoon == 0 and evening == 0:
                return super(op_time_frame, self).unlink(cr, uid, vals, context=context)
            else:
                raise osv.except_osv('You can not delete this record',
                                     'This Time Frame already referred in another location')

        return super(op_time_frame, self).unlink(cr, uid, vals, context=context)


class crm_tracking_campaign(osv.Model):
    _inherit = 'crm.tracking.campaign'
    _description = "adding fields to crm.lead"
    _columns = {
        'source_id': fields.many2many('crm.tracking.source', 'campaign_source_rel', 'campaign_id', 'source_id',
                                      'Source(s)'),
    }

    # ----------------Validations----------------------- s#
    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        campaign_name = str(name).replace(" ", "")
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        elif campaign_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Name !'), _('Please Enter a valid name'))

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        return super(crm_tracking_campaign, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        return super(crm_tracking_campaign, self).write(cr, uid, ids, values, context=context)


class crm_tracking_source(osv.Model):
    _inherit = 'crm.tracking.source'
    _description = "adding fields to crm.lead"
    _columns = {
        'channel_id': fields.many2one('crm.tracking.medium', 'Channel'),
    }

    # ----------------Validations----------------------- s#
    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        channel_name = str(name).replace(" ", "")
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Source Name !'), _('Only Spaces not allowed'))
        elif channel_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Source Name !'), _('Please Enter a valid name'))

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        return super(crm_tracking_source, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        return super(crm_tracking_source, self).write(cr, uid, ids, values, context=context)

class crm_tracking_medium(osv.Model):
    _inherit = 'crm.tracking.medium'

    # ----------------Validations----------------------- s#
    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        channel_name = str(name).replace(" ", "")
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        elif channel_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Name !'), _('Please Enter a valid name'))

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        return super(crm_tracking_medium, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        return super(crm_tracking_medium, self).write(cr, uid, ids, values, context=context)


class op_follow_up_type(osv.Model):

    _name = 'op.follow.up.type'
    _columns = {
        'code': fields.char('Code', required=True, size=4),
        'name': fields.char('Name', required=True, size=30)
    }

    _sql_constraints = [('name', 'UNIQUE (name)', 'The Name of the Type must be unique!')]

    # ----------------Validations----------------------- s#
    # ---------code validation------------- s#
    def code_validation(self, cr, uid, ids, code):
        follow_up_type_code = str(code).replace(" ", "")
        follow_type_code = ''.join([i for i in follow_up_type_code if not i.isdigit()])
        lengthTypeCode = len(code)
        if lengthTypeCode >= 2 and follow_type_code.isalpha() and follow_up_type_code.isdigit():
            return True
        else:
            if lengthTypeCode <= 2:
                raise osv.except_osv(_('Invalid Code !'), _('Minimum data length should be at least 2 characters'))
            else:
                if str(code).isspace():
                    raise osv.except_osv(_('Invalid Code !'), _('Only Spaces not allowed'))
                elif follow_type_code.isalpha() or follow_up_type_code.isdigit():
                    return True
                else:
                    raise osv.except_osv(_('Invalid Code !'), _('Please Enter the code correctly'))

    # def code_validation(self, cr, uid, ids, code):
    #     crm_tag_code = str(code).replace(" ", "")
    #     crm_tag_new_code = ''.join([i for i in crm_tag_code if not i.isdigit()])
    #     lengthTagsCode = len(code)
    #     if lengthTagsCode >= 2 and crm_tag_new_code.isalpha() and crm_tag_code.isdigit():
    #         return True
    #     else:
    #         if lengthTagsCode <= 2:
    #             raise osv.except_osv(_('Invalid Code !'), _('Minimum data length should be at least 2 characters'))
    #         else:
    #             if str(code).isspace():
    #                 raise osv.except_osv(_('Invalid Code !'), _('Only Spaces not allowed'))
    #             elif crm_tag_new_code.isalpha() or crm_tag_code.isdigit():
    #                 return True
    #             else:
    #                 raise osv.except_osv(_('Invalid Code !'), _('Please Enter the code correctly'))

    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        follow_up_type_name = str(name).replace(" ", "")
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        elif follow_up_type_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Name !'), _('Please Enter a valid name'))

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------code validation caller------- s#
        if 'code' in vals:
            self.code_validation(cr, uid, [], vals['code'])

        # ----------name validation caller------- s#
        if 'name' in vals:
            name = vals['name']
            s = self.pool.get('op.follow.up.type')  # get reference to object
            # Validate Followups duplicating
            get_name = s.search(cr, uid, [('name', '=', name)], count=True, context=context)
            if get_name > 0:
                raise osv.except_osv(_(u'Error'), _(u'Followup Type Already Exist!'))
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        code = vals['code'].strip().upper().replace(" ", "")
        name = vals['name'].strip().title()
        vals.update({'code': code, 'name': name})

        return super(op_follow_up_type, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # ----------code validation caller-------- s#
        if 'code' in values:
            self.code_validation(cr, uid, [], values['code'])

        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        # ------ update the values after removing white spaces---- s#
        if 'name' in values:
            name = values['name'].strip().title()
            values.update({'name': name})
        if 'code' in values:
            code = values['code'].strip().upper().replace(" ", "")
            values.update({'code': code})

        return super(op_follow_up_type, self).write(cr, uid, ids, values, context=context)

    def unlink(self, cr, uid, vals, context=None):
        #When delete followups update meeting count
        crmLead = self.pool.get('crm.lead')
        for values in vals:
            k = [values]
            cr.execute('SELECT id FROM calendar_event ' \
                        'WHERE type = %s ', (k))

            calendar_event_id = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            if calendar_event_id:
                int_calendar_event_id = int(calendar_event_id[0].id)
                list_int_calendar_event_id = [int_calendar_event_id]
                tags = len(list_int_calendar_event_id)
            else:
                tags = 0

            if tags == 0:
                return super(op_follow_up_type, self).unlink(cr, uid, vals, context=context)
            else:
                raise osv.except_osv('You can not delete this record', 'This Type already referred in another location')

        return super(op_follow_up_type, self).unlink(cr, uid, vals, context=context)


class crm_lead(osv.Model):

    # check prospective_student limit
    def _check_pstudent(self, cr, uid, ids, prospective_student):
        if prospective_student > 999:
            raise osv.except_osv('Prospective Students', 'Limit exceeded !')
        elif prospective_student < 1:
            raise osv.except_osv('Prospective Students', 'Cannot be Less than 1   !')
        else:
            return True

    _inherit = 'crm.lead'
    _rec_name = 'name'
    _description = "adding fields to crm.lead"

    def _meeting_count(self, cr, uid, ids, field_name, arg, context=None):
        Event = self.pool['calendar.event']
        return {
            opp_id: Event.search_count(cr, uid, [('opportunity_id', '=', opp_id)], context=context)
            for opp_id in ids
        }

    _columns = {
        'name': fields.char(string='Subject', size=57, select=1),
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='set null', track_visibility='onchange',
                                      select=True,
                                      help="Linked student (optional). Usually created when converting the lead.",
                                      domain="[('is_student', '=', True)]"),
        'modes': fields.many2one('op.lead.modes', 'Mode of Inquiry', required=True),
        'courses_interested': fields.many2many('op.study.programme', 'op_study_programme_lead_rel', 'lead_id',
                                               'study_programme_id',
                                               'Study programme(s) Interested'),
        'anytime': fields.many2many('op.time.frame', 'op_anytime_time_frame_rel', 'lead_id', 'time_frame_id',
                                    'Anytime'),
        'morning': fields.many2many('op.time.frame', 'op_morning_time_frame_rel', 'lead_id', 'time_frame_id',
                                    'Morning'),
        'afternoon': fields.many2many('op.time.frame', 'op_afternoon_time_frame_rel', 'lead_id', 'time_frame_id',
                                      'Afternoon'),
        'evening': fields.many2many('op.time.frame', 'op_evening_time_frame_rel', 'lead_id', 'time_frame_id',
                                    'Evening'),
        'prospective_student': fields.integer(size=5, string='No.of Prospective Students'),
        'inquiry_date': fields.date(string='Inquiry Date', required=True),
        'tags': fields.many2many('op.course.tags', 'op_crm_lead_tags_rel', 'lead_id', 'tag_id', 'New Study Programme Tags'),
        'address_line1': fields.char('address line1', size=20),
        'address_line2': fields.char('address line2', size=25),
        'town': fields.char('town', size=25),
        'province': fields.char('province', size=20),
        'nation': fields.char('nation', size=20),
        'meeting_count': fields.integer(string='No.Of Follow-ups'),
        # 'meeting_count': fields.function(_meeting_count,type='integer', string='#Follow-ups', store=True),

        'first_name': fields.char('First Name', size=30, required=True),
        'last_name': fields.char('Last Name', size=30, required=True),
        'probability': fields.float(string='Probability', readonly=True),
        'campaign_id': fields.many2one('crm.tracking.campaign', 'Campaign',  # old domain ="['|',('section_id','=',section_id),('section_id','=',False)]"
                                       help="This is a name that helps you keep track of your different campaign efforts Ex: Fall_Drive, Christmas_Special"),
        'medium_id': fields.many2one('crm.tracking.medium', 'Channel', help="This is the method of delivery. Ex: Postcard, Email, or Banner Ad", oldname='channel_id'),
        'source_id': fields.many2one('crm.tracking.source', 'Source', domain="[('channel_id', '=', medium_id)]")

    }

    _defaults = {
        'prospective_student': 1
    }

    # ------check spaces in address line one---------#
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

    # ---------check inquiry date-------------- s#
    def _check_date(self, cr, uid, vals, inquiry_date):
        inquiry_date = dateutil.parser.parse(inquiry_date).date()
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        date_today = dateutil.parser.parse(today_date).date()
        if inquiry_date <= date_today:
            pass
        else:
            raise osv.except_osv(_('Inquiry Date..!'), _('Cannot add a future date..'))

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
        # for stage_id, lead_ids in stages_leads.items():
        #     self.write(cr, uid, lead_ids, {'stage_id': stage_id}, context=context)

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
                    'name': 'Student Registration',
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
                'name': 'Student Registration',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'op.registration',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
            }
            return value
        return True

    # Company name validator by s
    def companyNameValidation(self, cr, uid, ids, companyName):
        c_name = str(companyName).replace(" ", "")
        if str(companyName).isspace():
            raise osv.except_osv(_('Invalid Company Name'), _('Only spaces not allowed to save'))
        elif c_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Company Name'), _('Please enter Company name correctly'))

    # phone number validation for customer
    def phoneNumberValidation(self, cr, uid, ids, phoneNumber):
        phone_re = re.compile(ur'^(\+\d{1,1}[- ]?)?\d{10}$|(\+\d{1,1}[- ]?)?\d{9}$')
        valid_phone = False
        if phoneNumber is False:
            return True
        if phone_re.match(phoneNumber):
            valid_phone = True
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
            valid_mobile = True
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
        if str(subjectName).isspace():
            raise osv.except_osv(_('Invalid Subject Description !'), _('Only spaces not allowed'))
        else:
            pass

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
        if f_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Contact Name'), _('Please enter a correct Contact name'))

    # ---------Contact last name validation-------------- #
    def last_name_validation(self, cr, uid, ids, last_name):
        l_name = str(last_name).replace(" ", "")
        if l_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Contact Name'), _('Please enter a correct Contact name'))

    # -------Expected date validation------------------- s#
    def backdat_validation(self, cr, uid, ids, date):
        if date:
            now = datetime.datetime.today()
            today = now.strftime('%Y-%m-%d')
            date_today = dateutil.parser.parse(today).date()
            assigned_date = dateutil.parser.parse(date).date()
            if date_today < assigned_date:
                return True
            else:
                raise osv.except_osv(_('Invalid Expected Closing Date!'), _('Enter a Future Date..'))
        else:
            pass

    # ----------availability of programs and tags-------------- s#
    def check_tags_pro(self, cr, uid, ids, pro, tags):
        study_tags_len = len(tags[0][2])
        study_pro_len = len(pro[0][2])
        if study_pro_len < 1 and study_tags_len < 1:
            raise osv.except_osv(_('Missing Required Information'), _(
                'Required one Interested Study programme or one New Study Programme Tag in Study Prorgammes Info'))
        else:
            pass

    def create(self, cr, uid, vals, context=None):

        #Minus values are not allowed for the planned_revenue
        if 'planned_revenue' in vals:
            price = vals['planned_revenue']
            if price >= 0:
                pass
            else:
                raise osv.except_osv('Value Error', 'Minus values are not allowed for the Expected Revenue')

        # ----------company name validation caller by s------- #
        if 'partner_name' in vals:
            self.companyNameValidation(cr, uid, [], vals['partner_name'])

        # ----------contact first name validation caller by s------------- #
        if 'first_name' in vals:
            self.first_name_validation(cr, uid, [], vals['first_name'])

        # ----------contact last name validation caller by s-------------- #
        if 'last_name' in vals:
            self.last_name_validation(cr, uid, [], vals['last_name'])

        # -----------phone number validation caller by s------------------ #
        if 'phone' in vals:
            self.phoneNumberValidation(cr, uid, [], vals['phone'])

        # ---------- mobile number validation caller by s----------------- #
        if 'mobile' in vals:
            self.mobileNumberValidation(cr, uid, [], vals['mobile'])

        # --------------fax number validation caller by s----------------- #
        if 'fax' in vals:
            self.faxNumberValidation(cr, uid, [], vals['fax'])

        if 'name' in vals:
            self._check_invalid_data(cr, uid, [], vals['name'])

        # --------Expected date validation-------------------- s#
        if 'date_deadline' in vals:
            self.backdat_validation(cr, uid, [], vals['date_deadline'])

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

        # ------update name after strip------ s#
        name = vals['name'].strip()
        vals.update({'name': name})

        # ------update company name after strip()---- s#
        if 'partner_name' in vals:
            if vals['partner_name'] is not False:
                partner_name = vals['partner_name'].strip().title()
                vals.update({'partner_name': partner_name})
        else:
            pass

        if 'inquiry_date' in vals:
            a = vals['inquiry_date']
            pass_date = dateutil.parser.parse(a).date()
            pass_date = pass_date.strftime('%Y-%m-%d')
            vals.update({'inquiry_date': pass_date})

        # ----------update contact name---------- s#
        if 'first_name' in vals:
            if vals['first_name'] is not False:
                first_name = vals['first_name'].strip().title()
                vals.update({'first_name': first_name})
        else:
            pass

        # ----------update contact name---------- s#
        if 'last_name' in vals:
            if vals['last_name'] is not False:
                last_name = vals['last_name'].strip().title()
                vals.update({'last_name': last_name})
        else:
            pass

        # ------------validate inquiry date---------- s#
        if 'inquiry_date' in vals:
            if vals['inquiry_date'] is not False:
                self._check_date(cr, uid, [], vals['inquiry_date'])
        else:
            pass

        # ---------Check availability of study programme or tags--------- s#
        if 'courses_interested' in vals or 'tags' in vals:
            if vals['courses_interested'] is not False and vals['tags'] is False:
                pass
            elif vals['courses_interested'] is False and vals['tags'] is not False:
                pass
            elif vals['courses_interested'] is False and vals['tags'] is  False:
                raise osv.except_osv(_('Missing Required Information'), _('Required one Interested Study programme or one New Study Programme Tag in Study Prorgammes Info'))
            else:
                self.check_tags_pro(cr, uid, [], vals['courses_interested'], vals['tags'])


        # Almost required a value from email or mobile or phone
        if 'email_from' in vals or 'mobile' in vals or 'phone' in vals:
            email = vals['email_from']
            mobile = vals['mobile']
            phone = vals['phone']
            if email == False and mobile == False and phone == False:
                raise osv.except_osv(_('Missing Required Information'),
                                     _('Required Email or Mobile or Phone to contact.!'))
            else:
                pass

        return super(crm_lead, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, values, context=None):

        #Minus values are not allowed for the planned_revenue
        if 'planned_revenue' in values:
            price = values['planned_revenue']
            if price >= 0:
                pass
            else:
                raise osv.except_osv('Value Error', 'Minus values are not allowed for the Expected Revenue')

        # ----------company name validation caller by ------- s#
        if 'partner_name' in values:
            self.companyNameValidation(cr, uid, [], values['partner_name'])

        # ----contact first name validation function caller by s ----- #
        if 'first_name' in values:
            self.first_name_validation(cr, uid, [], values['first_name'])

        # -----contact last name validation function caller by s----- #
        if 'last_name' in values:
            self.last_name_validation(cr, uid, [], values['last_name'])

        # -----phone number validation on write function caller by s-- #
        if 'phone' in values:
            self.phoneNumberValidation(cr, uid, [], values['phone'])

        # -----mobile number validation function caller by s---------- #
        if 'mobile' in values:
            self.mobileNumberValidation(cr, uid, [], values['mobile'])

        # -----fax number validation function caller by s------------- #
        if 'fax' in values:
            self.faxNumberValidation(cr, uid, [], values['fax'])

        # --------Expected date validation-------------------- s#
        if 'date_deadline' in values:
            self.backdat_validation(cr, uid, [], values['date_deadline'])

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

        # ------------validate inquiry date---------- s#
        if 'inquiry_date' in values:
            if values['inquiry_date'] is not False:
                self._check_date(cr, uid, [], values['inquiry_date'])
        else:
            pass

        # -----------------Update Values--------------------- s#
        # ------update name------ s#
        if 'name' in values:
            name = values['name'].strip()
            values.update({'name': name})

        # ------update company name----- s#
        if 'partner_name' in values:
            if values['partner_name'] is not False:
                partner_name = values['partner_name'].strip().title()
                values.update({'partner_name': partner_name})
            else:
                pass

        # ----------update first name---------- s#
        if 'first_name' in values:
            if values['first_name'] is not False:
                first_name = values['first_name'].strip().title()
                values.update({'first_name': first_name})
            else:
                pass

        # ---------update last name------------ s#
        if 'last_name' in values:
            if values['last_name'] is not False:
                last_name = values['last_name'].strip().title()
                values.update({'last_name': last_name})
            else:
                pass

        # ---------Check availability of study programme or tags--------- s#
        if 'courses_interested' in values or 'tags' in values:
            cr.execute('SELECT tag_id FROM op_crm_lead_tags_rel WHERE lead_id=%s ', ids)
            tags_records = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            tags_length = len(tags_records)

            cr.execute('SELECT study_programme_id FROM op_study_programme_lead_rel WHERE lead_id=%s ', ids)
            std_records = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            stdy_length = len(std_records)

            if 'courses_interested' in values and 'tags' in values:
                if len(values['courses_interested'][0][2]) or len(values['tags'][0][2]):
                    pass
                else:
                    raise osv.except_osv(_('Error'), _('no length'))

            if 'courses_interested' in values and 'tags' not in values:
                if len(values['courses_interested'][0][2]):
                    pass
                elif tags_length > 0:
                    pass
                else:
                    raise osv.except_osv(_('Error'), _('no length'))

            if 'courses_interested' not in values and 'tags' in values:
                if len(values['tags'][0][2]):
                    pass
                elif stdy_length > 0:
                    pass
                else:
                    raise osv.except_osv(_('Error'), _('no length'))

        return super(crm_lead, self).write(cr, uid, ids, values, context=context)

    _constraints = [
        (_check_add_l_one, 'Entered Invalid Data in Address line1 !!', ['address_line1']),
        (_check_add_l_two, 'Entered Invalid Data in Address line2 !!', ['address_line2']),
        (_check_town, 'Entered Invalid Data in City !!', ['town']),
        (_check_province, 'Entered Invalid Data in Province !!', ['province']),
        (_check_nation, 'Entered Invalid Data in Country !!', ['nation']),
    ]


class calendar_event(osv.Model):
    _inherit = 'calendar.event'
    _columns = {
        'type': fields.many2one('op.follow.up.type', 'Follow-up Type', required=True)
    }

    def copy(self, cr, uid, id, default=None, context=None):
        raise osv.except_osv(_('Forbbiden to duplicate'), _('Is not possible to duplicate the record, please create a new one.'))

    # ---------repetition validation------------- #
    def _check_repetitions(self, cr, uid, ids, count):
        if count == 0:
            raise osv.except_osv('Number of repetitions', 'Invalid Value !')
        elif count > 999:
            raise osv.except_osv('Number of repetitions', 'Limit exceeded ( Maximum 3 digits )!')
        else:
            return True

    # ---------repeat validation------------- #
    def _check_repeat(self, cr, uid, ids, interval):
        if interval == 0:
            raise osv.except_osv('Number of repeats', 'Invalid Value ! !')
        elif interval > 999:
            raise osv.except_osv('Number of repeat', 'Limit exceeded ( Maximum 3 digits )!')
        else:
            return True

    def default_get(self, cr, uid, fields, context=None):
        data = super(calendar_event, self).default_get(cr, uid, fields, context=context)
        activeId = context.get('active_id')
        if activeId:
            data['opportunity_id'] = activeId
        return data

    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        sub_name = str(name).replace(" ", "")
        sub_name = ''.join([i for i in sub_name if not i.isdigit()])
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        elif sub_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Name !'), _('Please Enter a valid name'))

    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        name = vals['name'].strip().title()
        vals.update({'name': name})

        #When create a followup update the FollowUp counts in CRM Lead
        if len(context) != 0:
            activeID = context['active_id']

            calenderEvent = self.pool.get('calendar.event')
            crmLead = self.pool.get('crm.lead')

            calenderEventId = calenderEvent.search(cr, uid, [('opportunity_id', '=', activeID)])
            lengthCalenderEventId = len(calenderEventId)
            meetingCount = lengthCalenderEventId + 1

            if lengthCalenderEventId == 0:
                crmLead.write(cr, uid, [activeID], {'meeting_count': meetingCount})
            else:
                crmLead.write(cr, uid, [activeID], {'meeting_count': meetingCount})
        else:
            pass

            # ------repetition validation on create---------------------- #
        if 'count' in vals:
            self._check_repetitions(self, cr, uid, vals['count'])

        # ------repeat validation on create---------------------- #
        if 'interval' in vals:
            self._check_repeat(self, cr, uid, vals['interval'])

        return super(calendar_event, self).create(cr, uid, vals, context=context)

    # -----------Override the write method-------------- s#
    def write(self, cr, uid, ids, values, context=None):
        # -----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        # ------ update the values after removing white spaces---- s#
        if 'name' in values:
            name = values['name'].strip().title()
            values.update({'name': name})

         # ------repetition validation on write---------------------- #
        if 'count' in values:
            self._check_repetitions(self, cr, uid, values['count'])

        # ------repeat validation on write---------------------- #
        if 'interval' in values:
            self._check_repeat(self, cr, uid, values['interval'])


        return super(calendar_event, self).write(cr, uid, ids, values, context=context)

    def unlink(self, cr, uid, vals, context=None):
        #When delete followups update meeting count
        crmLead = self.pool.get('crm.lead')
        for calenderventID in vals:
            listCalenderventID = [calenderventID]
            cr.execute('SELECT opportunity_id FROM calendar_event ' \
                       'WHERE id=%s ', (listCalenderventID))

            opportunityId = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            intOpportunityId = int(opportunityId[0].id)
            listIntOpportunityId = [intOpportunityId]

            cr.execute('SELECT meeting_count FROM crm_lead ' \
                       'WHERE id=%s ', (listIntOpportunityId))

            meetingCount = crmLead.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            intMeetingCount = int(meetingCount[0].id)

            updateMeetingCount = intMeetingCount - 1
            crmLead.write(cr, uid, [intOpportunityId], {'meeting_count': updateMeetingCount})

        return super(calendar_event, self).unlink(cr, uid, vals, context=context)

    # def write(self, cr, uid, ids, values, context=None):
    #
    #     # ------repetition validation on write---------------------- #
    #     if 'count' in values:
    #         self._check_repetitions(self, cr, uid, values['count'])
    #
    #     # ------repeat validation on write---------------------- #
    #     if 'interval' in values:
    #         self._check_repeat(self, cr, uid, values['interval'])
    #
    #     return super(calendar_event, self).write(cr, uid, ids, values, context=context)
calendar_event()


class crm_case_stage(osv.Model):
    _inherit = 'crm.case.stage'

    # ------------------Validations----------------------- s#
    # ------------name validation--------------- s#
    def name_validation(self, cr, uid, ids, name):
        dup_name = str(name).strip().title()
        name_val = str(name).replace(" ", "")
        dup_val = self.pool.get("crm.case.stage").search(cr, uid, [('name', '=', dup_name)])
        if str(name).isspace():
            raise osv.except_osv(_('Name Field..'), _('Only Spaces not allowed..!'))
        elif len(dup_val) > 0:
            raise osv.except_osv(_('Data Duplication..!'), _('Name value already exists'))
        elif not name_val.isalpha():
            raise osv.except_osv(_('Name Field..'), _('Special Characters and Numbers not allowed'))
        else:
            pass

            # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        name = vals['name'].strip().title()
        vals.update({'name': name})

        return super(crm_case_stage, self).create(cr, uid, vals, context=context)

    # ------------Override the write method----------- s#
    def write(self, cr, uid, values, context=None):
        # ----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        # --------removing white spaces---------- s#
        name = values['name'].strip().title()
        values.update({'name': name})

        return super(crm_case_stage, self).write(cr, uid, values, values, context=context)

    def unlink(self, cr, uid, vals, context=None):
        for calenderventID in vals:
            listCalenderventID = [calenderventID]

            cr.execute('SELECT COUNT(id) FROM crm_lead ' \
                       'WHERE stage_id=%s ', (listCalenderventID))

            opportunityId = self.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
            intMeetingCount = int(opportunityId[0].id)
            if intMeetingCount == 0:
                return super(crm_case_stage, self).unlink(cr, uid, vals, context=context)
            else:
                raise osv.except_osv('You can not delete this record',
                                     'This Stage already referred in another location')

crm_case_stage()

class crm_case_categ(osv.Model):
    _inherit = 'crm.case.categ'

    # ------------------Validations----------------------- s#
    # ------------name validation--------------- s#
    def name_validation(self, cr, uid, ids, name):
        dup_name = str(name).strip().title()
        name_val = str(name).replace(" ", "")
        dup_val = self.pool.get("crm.case.categ").search(cr, uid, [('name', '=', dup_name)])
        if str(name).isspace():
            raise osv.except_osv(_('Name Field..'), _('Only Spaces not allowed..!'))
        elif len(dup_val) > 0:
            raise osv.except_osv(_('Data Duplication..!'), _('Name value already exists'))
        elif not name_val.isalpha():
            raise osv.except_osv(_('Name Field..'), _('Special Characters or Numbers not allowed'))
        else:
            pass

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------name validation caller------- s#
        if 'name' in vals:
            if 'name' in vals:
                name = vals['name']
                get_dul = self.pool.get('crm.case.stage').search(cr, uid, ['name', '=', name], context=context)
                if len(get_dul) == 1:
                    raise osv.except_osv(_(u'Error'), _(u'Same Stage Already exist.'))
                return
            else:
                return True
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        name = vals['name'].strip().title()
        vals.update({'name': name})

        return super(crm_case_categ, self).create(cr, uid, vals, context=context)

    # ------------Override the write method----------- s#
    def write(self, cr, uid, values, context=None):
        # ----------name validation caller------- s#
        if 'name' in values:
            self.name_validation(cr, uid, [], values['name'])

        # --------removing white spaces---------- s#
        name = values['name'].strip().title()
        values.update({'name': name})

        return super(crm_case_categ, self).write(cr, uid, values, context=context)


# class crm_partner_binding(osv.osv_memory):
#     _inherit = 'crm.partner.binding'
#
#     def create(self, cr, uid, vals, context=None):
#         # ----------name validation caller------- s#
#         if 'name' in vals:
#             if 'name' in vals:
#                 name = vals['name']
#                 get_dul = self.pool.get('crm.case.stage').search(cr, uid, ['name', '=', name], context=context)
#                 if len(get_dul) == 1:
#                     raise osv.except_osv(_(u'Error'), _(u'Same Stage Already exist.'))
#                 return
#             else:
#                 return True
#             self.name_validation(cr, uid, [], vals['name'])
#
#         # --------removing white spaces---------- s#
#         name = vals['name'].strip().title()
#         vals.update({'name': name})
#
#         return super(crm_case_categ, self).create(cr, uid, vals, context=context)
#
# crm_partner_binding()

