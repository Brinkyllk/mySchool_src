# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################
from openerp.osv import osv, fields
import time
from openerp import netsvc, api
from openerp.tools.translate import _
from datetime import date, datetime
import dateutil
from dateutil import parser

class op_registration(osv.osv):

    # --First name first letter capitalization--- #
    @api.onchange('first_name')
    def onchange_fname(self, cr, uid, ids, first_name):
        if first_name != False:
            result = {'value': {
                'first_name': str(first_name).title()
            }
            }
            return result
        else:
            return True

    # --Middle name first letter capitalization--- #
    @api.onchange('middle_name')
    def onchange_mname(self, cr, uid, ids, middle_name):
        if middle_name != False:
            result = {'value': {
                'middle_name': str(middle_name).title()
            }
            }
            return result
        else:
            return True

    # --Last name first letter capitalization--- #
    @api.onchange('last_name')
    def onchange_lname(self, cr, uid, ids, last_name):
        if last_name != False:
            result = {'value': {
                'last_name': str(last_name).title()
            }
            }
            return result
        else:
            return True

    _name = 'op.registration'
    _rec_name = 'application_number'

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'd',
            'application_number': self.pool.get('ir.sequence').get(cr, uid, 'op.registration'),
        })
        return super(op_registration, self).copy(cr, uid, id, default, context=context)

    _columns = {
        'first_name': fields.char(size=15, string='First Name', required=True, states={'done': [('readonly', True)]}),
        'middle_name': fields.char(size=15, string='Middle Name',
                                   states={'done': [('readonly', True)]}),
        'last_name': fields.char(size=20, string='Last Name', required=True, states={'done': [('readonly', True)]}),
        'title': fields.many2one('res.partner.title', 'Title', states={'done': [('readonly', True)]}),
        'application_number': fields.char(size=16, string='Application Number', required=True, readonly=True),
        'registration_date': fields.date(string='Registration Date', required=True, states={'done': [('readonly', True)]}),
        'application_date': fields.datetime(string='Application Date', required=True,
                                            states={'done': [('readonly', True)]}),
        'birth_date': fields.date(string='Birth Date', required=True, states={'done': [('readonly', True)]}),

        'address_line1': fields.char('address line1', size=20, states={'done': [('readonly', True)]}),
        'address_line2': fields.char('address line2', size=25, states={'done': [('readonly', True)]}),
        'town': fields.char('town', size=25, states={'done': [('readonly', True)]}),
        'province': fields.char('province', size=20, states={'done': [('readonly', True)]}),
        'nation': fields.char('nation', size=20, states={'done': [('readonly', True)]}),

        'fees': fields.float(string='Fees', digits=(2, 2), states={'done': [('readonly', True)]}),
        'photo': fields.binary(string='Photo', states={'done': [('readonly', True)]}),
        'state': fields.selection(
            [('d', 'Draft'), ('done', 'Done'), ('r', 'Rejected'),
             ('c', 'Cancel')], readonly=True, select=True, string='State'),
        'due_date': fields.date(string='Due Date', states={'done': [('readonly', True)]}),
        'family_business': fields.char(size=100, string='Family Business', states={'done': [('readonly', True)]}),
        'family_income': fields.float(string='Family Income', states={'done': [('readonly', True)]}),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', required=True,
                                   states={'done': [('readonly', True)]}),
        'division_id': fields.many2one('op.division', string='Division', states={'done': [('readonly', True)]}),
        'student_id': fields.many2one('op.student', string='Student', states={'done': [('readonly', True)]}),
        'nbr': fields.integer('# of Registration', readonly=True),
        'lead_id': fields.integer('Lead Id'),
        #course enrollment for the specific registration
        'enrollment_ids': fields.one2many('op.enrollment', 'reg_id', string='Registered Courses', required=True)
    }

    _defaults = {
        'application_number': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.registration'),
        'state': 'd',
        'registration_date': time.strftime('%Y-%m-%d'),
        'application_date': time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    _order = "application_number desc"


    # def due_backdate_validation(self, cr, uid, ids, date):
    #     if date:
    #         now = datetime.datetime.today()
    #         today = now.strftime('%Y-%m-%d')
    #         date_today = dateutil.parser.parse(today).date()
    #         assigned_date = dateutil.parser.parse(date).date()
    #         if date_today <= assigned_date:
    #             return True
    #         else:
    #             raise osv.except_osv(_('Invalid Expected Closing Date!'), _('Enter a Future Date..'))
    #     else:
    #         pass

    def default_get(self, cr, uid, fields, context=None):
        data = super(op_registration, self).default_get(cr, uid, fields, context=context)
        activeId = context.get('active_id')
        if activeId:

            registrationRef = self.pool.get('crm.lead')
            registrationId = registrationRef.browse(cr, uid, activeId, context=context)

            data['first_name'] = registrationId.first_name
            data['last_name'] = registrationId.last_name
            data['lead_id'] = activeId

        return data

    def confirm_rejected(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'r'})
        return True

    # def confirm_pending(self, cr, uid, ids, context=None):
    #     self.write(cr, uid, ids, {'state': 'p'})
    #     return True

    def confirm_to_draft(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        self.write(cr, uid, ids, {'state': 'd'})
        for inv_id in ids:
            wf_service.trg_delete(uid, 'op.registration', inv_id, cr)
            wf_service.trg_create(uid, 'op.registration', inv_id, cr)
        return True

    def confirm_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'c'})
        return True

    def confirm_selection(self, cr, uid, ids, context={}):
        # this_obj = self.browse(cr, uid, ids[0], context)
        # student = self.pool.get('op.student').browse(cr, uid, this_obj.student_id.id, context)
        models_data = self.pool.get('ir.model.data')
        form_view = models_data.get_object_reference(cr, uid, 'myschool', 'view_student_form')
        tree_view = models_data.get_object_reference(cr, uid, 'myschool', 'view_student_tree')
        field = self.browse(cr, uid, ids, context=context)

        enrollmentRef = self.pool.get('op.enrollment')
        id = ids[0]
        enrollmentId = enrollmentRef.search(cr, uid, [('reg_id', '=', id)])
        enrollmentRealId = enrollmentRef.browse(cr, uid, enrollmentId, context=context)

        value = {
            # 'domain': str([('id', '=', student.id)]),
            'name': 'Student Profile',
            # "version": "7.0",
            'view_type': 'form',
            'view_mode': 'form, tree',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view[1] or False, 'form'),
                      (tree_view and tree_view[1] or False, 'tree')],
            'type': 'ir.actions.act_window',
            # 'res_id': student.id,
            'target': 'new',
            'flags': {'action_buttons': True},
            'context': context,
            }

        self.write(cr, uid, ids, {'state': 'done'})

        for x in enrollmentRealId:
            courseEnrollmentId = x.id
            isStudent = enrollmentRef.read(cr, uid, courseEnrollmentId, ['confirm'])
            confirm = isStudent.get('confirm')
            if confirm == True:
                return value
        else:
            raise osv.except_osv(_(u'Error'), _(u'Please confirm a course to Enroll'))

    # .... check first name....#
    def _check_invalid_first_name(self, cr, uid, ids, firstName):
        name = str(firstName)
        if name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid first name'), _('Please insert valid name'))

    # .... check middle name....#
    def _check_invalid_middle_name(self, cr, uid, ids,middleName):
        name = str(middleName)
        if name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid middle name'), _('Please insert valid name'))

    # .... check last name....#
    def _check_invalid_last_name(self, cr, uid, ids, lastName):
        name = str(lastName)
        if name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid last name'), _('Please insert valid name'))

    # ....birthday validation.... #
    def _check_birthday(self, cr, uid, ids, birthDate):
        date_today = date.today()
        if birthDate and date_today:
            datetime_format = "%Y-%m-%d"
            bday = datetime.strptime(birthDate, datetime_format)
            tday = datetime.strptime(date_today.strftime('%Y%m%d'), '%Y%m%d')
            if tday < bday:
                raise osv.except_osv(_('Invalid Birth Date'), _('Please insert valid Birth Date'))
            else:
                return True

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

    #-----check spaces in town-----------------#
    def _check_town(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.town)
        if not value:
            return False
        else:
            return True

    #-----check spaces in province--------------#
    def _check_province(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.province)
        if not value:
            return False
        else:
            return True

    #-----check spaces in country---------------#
    def _check_nation(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        value = str(obj.nation)
        new_value = value.replace(" ", "")
        if not new_value or not new_value.isalpha():
            return False
        else:
            return True

    def create(self, cr, uid, vals, context=None):

        # phone number validation on create
        if 'first_name' in vals:
            self._check_invalid_first_name(cr, uid, [], vals['first_name'])

        if 'middle_name' in vals:
            self._check_invalid_middle_name(cr, uid, [], vals['middle_name'])

        if 'last_name' in vals:
            self._check_invalid_last_name(cr, uid, [], vals['last_name'])

        if 'birth_date' in vals:
            self._check_birthday(cr, uid, [], vals['birth_date'])

        if vals['due_date'] != False:
            if 'due_date' in vals:
                reg_date = vals['registration_date']
                apl_date = vals['application_date']
                due_date = vals['due_date']
                reg_date = dateutil.parser.parse(reg_date).date()
                apl_date = dateutil.parser.parse(apl_date).date()
                due_date = dateutil.parser.parse(due_date).date()
                if due_date > reg_date and due_date > apl_date:
                    pass
                else:
                    raise osv.except_osv(_('Due Date Error'), _('Due date cannot be back date to Registration and Application dates'))

        # Address lines and update res.partner
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

        k = vals['lead_id']
        print k
        leadref = self.pool.get('crm.lead')
        # leadref.write(cr, uid, k, {'stage_id': 6}, context=context)
        leadref.write(cr, uid, [k],{ 'stage_id': 6})

        # return super(op_registration, self).create(cr, uid, vals, context=context)

        # -----Check whether enrollment has or not------- #
        reg_id = super(op_registration, self).create(cr, uid, vals, context=context)
        enrollment_ref = self.pool.get('op.enrollment')
        enrollment_count = enrollment_ref.search(cr, uid, [('reg_id', '=', reg_id)], count=True, context=context)
        if enrollment_count < 1:
            raise osv.except_osv(_(u'Error'), _(u'Make an Enrollment'))

        return reg_id

    def write(self, cr, uid, ids, values, context=None):

        # phone number validation on write
        if 'first_name' in values:
            self._check_invalid_first_name(cr, uid, [], values['first_name'])

        if 'middle_name' in values:
            self._check_invalid_middle_name(cr, uid, [], values['middle_name'])

        if 'last_name' in values:
            self._check_invalid_last_name(cr, uid, [], values['last_name'])

        if 'birth_date' in values:
            self._check_birthday(cr, uid, [], values['birth_date'])

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

        return super(op_registration, self).write(cr, uid, ids, values, context=context)

    _constraints = [
        (_check_add_l_one, 'Entered Invalid Data in Address line1 !!', ['address_line1']),
        (_check_add_l_two, 'Entered Invalid Data in Address line2 !!', ['address_line2']),
        (_check_town, 'Entered Invalid Data in City !!', ['town']),
        (_check_province, 'Entered Invalid Data in Province !!', ['province']),
        (_check_nation, 'Entered Invalid Data in Country !!', ['nation']),
        ]
op_registration()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

