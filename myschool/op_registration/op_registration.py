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
from openerp import netsvc


class op_registration(osv.osv):
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
        'application_number': fields.char(size=16, string='Application Number', required=True,
                                          states={'done': [('readonly', True)]}),
        'registration_date': fields.date(string='Registration Date', required=True, states={'done': [('readonly', True)]}),
        'application_date': fields.datetime(string='Application Date', required=True,
                                            states={'done': [('readonly', True)]}),
        'birth_date': fields.date(string='Birth Date', required=True, states={'done': [('readonly', True)]}),

        'address_line1': fields.char('address line1', size=20, states={'done': [('readonly', True)]}),
        'address_line2': fields.char('address line2', size=25, states={'done': [('readonly', True)]}),
        'town': fields.char('town', size=25, states={'done': [('readonly', True)]}),
        'province': fields.char('province', size=20, states={'done': [('readonly', True)]}),
        'nation': fields.char('nation', size=20, states={'done': [('readonly', True)]}),

        'fees': fields.float(string='Fees', states={'done': [('readonly', True)]}),
        'photo': fields.binary(string='Photo', states={'done': [('readonly', True)]}),
        'state': fields.selection(
            [('d', 'Draft'), ('done', 'Done'), ('r', 'Rejected'),
             ('c', 'Cancel')], readonly=True, select=True, string='State'),
        'due_date': fields.date(string='Due Date', states={'done': [('readonly', True)]}),
        'family_business': fields.char(size=256, string='Family Business', states={'done': [('readonly', True)]}),
        'family_income': fields.float(string='Family Income', states={'done': [('readonly', True)]}),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', required=True,
                                   states={'done': [('readonly', True)]}),
        'division_id': fields.many2one('op.division', string='Division', states={'done': [('readonly', True)]}),
        'student_id': fields.many2one('op.student', string='Student', states={'done': [('readonly', True)]}),
        'nbr': fields.integer('# of Registration', readonly=True),
        # 'enrollment_ids': fields.one2many('op.enrollment', 'student_id', string='Registered Courses'),
    }

    _defaults = {
        'application_number': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.registration'),
        'state': 'd',
        'registration_date': time.strftime('%Y-%m-%d'),
        'application_date': time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    _order = "application_number desc"

    # def confirm_in_progress(self, cr, uid, ids, context=None):
    #     self.write(cr, uid, ids, {'state': 'i'})
    #     return True

    # def confirm_selection(self, cr, uid, ids, context=None):
    #     if context is None:
    #         context = {}
    #     student_pool = self.pool.get('op.student')
    #
    #     for field in self.browse(cr, uid, ids, context=context):
    #         vals = {
    #             'title': field.title and field.title.id or False,
    #             'first_name': field.first_name,
    #             'middle_name': field.middle_name,
    #             'last_name': field.last_name,
    #             'birth_date': field.birth_date,
    #             'gender': field.gender,
    #             'photo': field.photo or False,
    #             'address_line1': field.address_line1 or False,
    #             'address_line2': field.address_line2 or False,
    #             'town': field.town or False,
    #             'province': field.province or False,
    #             'nation': field.nation or False,
    #         }
    #
    #     new_student = student_pool.create(cr, uid, vals, context=context)
    #     self.write(cr, uid, ids, {'state': 's', 'student_id': new_student, 'nbr': 1})
    #     return True

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
        value = {
            # 'domain': str([('id', '=', student.id)]),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.student',
            # 'view_id': 'op_student_form_view_extended',
            'views': [(form_view and form_view[1] or False, 'form'),
                      (tree_view and tree_view[1] or False, 'tree')],
            'res_id': ids[0],
            'target': 'new',
            'nodestroy': True,
            'context': context,
            }
        self.write(cr, uid, ids, {'state': 'done'})
        return value

op_registration()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


# class op_student(osv.Model):
#     _inherit = 'op.student'
#     _description = "create a new student"
#     _columns = {
#
#     }

    # def default_get(self, cr, uid, fields, context=None):
    #     data = super(op_student, self).default_get(cr, uid, fields, context=context)
    #     activeId = context.get('active_id')
    #
    #     registrationRef = self.pool.get('op.registration')
    #     registrationId = registrationRef.browse(cr, uid, activeId, context=context)
    #
    #     data['title'] = registrationId.title.id
    #     data['first_name'] = registrationId.first_name
    #     data['middle_name'] = registrationId.middle_name
    #     data['last_name'] = registrationId.last_name
    #     data['birth_date'] = registrationId.birth_date
    #     data['gender'] = registrationId.gender
    #     data['photo'] = registrationId.photo
    #     data['address_line1'] = registrationId.address_line1
    #     data['address_line2'] = registrationId.address_line2
    #     data['town'] = registrationId.town
    #     data['province'] = registrationId.province
    #     data['nation'] = registrationId.nation
    #
    #     return data

    # def create(self, cr, uid, vals, context=None):
    #     if 'first_name' in vals:
    #         fname = vals['first_name'].strip()
    #         vals.update({'first_name': fname})
    #
    #     if 'middle_name' in vals:
    #         if vals['middle_name'] is False or None:
    #             pass
    #         else:
    #             mi_name = vals['middle_name'].strip()
    #             vals.update({'middle_name': mi_name})
    #
    #     if 'last_name' in vals:
    #         lname = vals['last_name'].strip()
    #         vals.update({'last_name': lname})
    #
    #     if 'initials' in vals:
    #         if vals['initials'] is False or None:
    #             pass
    #         else:
    #             initls = vals['initials'].strip()
    #             vals.update({'initials': initls})
    #
    #     # phone number validation on create
    #     if 'phone' in vals:
    #         self.phoneNumberValidation(cr, uid, [], vals['phone'])
    #     if 'contact_no' in vals:
    #         self.phoneNumberValidationParent(cr, uid, [], vals['contact_no'])
    #
    #     # Clean NIC
    #     if 'id_number' in vals:
    #         try:
    #             vals['id_number'] = vals['id_number'].strip()
    #             if vals['id_number'] == '':
    #                 vals['id_number'] = None
    #         except:
    #             vals['id_number'] = None
    #
    #     # Fix initials if empty
    #     try:
    #         initials = vals['initials'].strip()
    #     except Exception:
    #         initials = ''
    #         pass
    #
    #     if initials == '':
    #         full_name = vals['first_name'].strip() + ' ' + vals['last_name'].strip()
    #     else:
    #         full_name = vals['initials'] + ' ' + vals['first_name'].strip() + ' ' + vals['last_name'].strip()
    #     vals.update({'name': full_name})  # Update Partner record
    #
    #     # Address lines and update res.partner
    #     if 'address_line1' in vals:
    #         if vals['address_line1'] is False or None:
    #             pass
    #         else:
    #             line1 = vals['address_line1'].strip()
    #             vals.update({'street': line1, 'address_line1': line1})
    #
    #     if 'address_line2' in vals:
    #         if vals['address_line2'] is False or None:
    #             pass
    #         else:
    #             line2 = vals['address_line2'].strip()
    #             vals.update({'street2': line2, 'address_line2': line2})
    #
    #     if 'town' in vals:
    #         if vals['town'] is False or None:
    #             pass
    #         else:
    #             twn = vals['town'].strip()
    #             vals.update({'city': twn, 'town': twn})
    #
    #     if 'province' in vals:
    #         if vals['province'] is False or None:
    #             pass
    #         else:
    #             prvn = vals['province'].strip()
    #             vals.update({'province': prvn})
    #
    #     if 'nation' in vals:
    #         if vals['nation'] is False or None:
    #             pass
    #         else:
    #             cntry = vals['nation'].strip()
    #             vals.update({'nation': cntry})
    #
    #     # Get student ID
    #     vals['stu_reg_number'] = self.pool.get('ir.sequence').get(cr, uid, 'myschool.op_student') or '/'
    #     vals.update({'is_student': True})  # Partner type is student
    #     # vals.update({'stu_reg_id': vals['stu_reg_number']})  # Support backwards compatible
    #
    #     # email validation on create
    #     if 'email' in vals:
    #         self.validate_email(cr, uid, [], vals['email'])
    #
    #     if 'last_name' in vals:
    #         self.validate_last_name(cr, uid, [], vals['last_name'])
    #
    #     if 'middle_name' in vals:
    #         self.validate_middle_name(cr, uid, [], vals['middle_name'])
    #
    #     # NIC validation on create
    #     if 'id_number' in vals:
    #         self.validate_NIC(cr, uid, [], vals['id_number'])
    #
    #     if 'is_company' in vals:
    #         if vals['is_company'] == True:
    #             if vals['register_date'] == False or vals['register_date'] == None:
    #                 raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a Registered Date..!!')
    #         else:
    #             if vals['birth_date'] == False or vals['birth_date'] == None:
    #                 raise osv.except_osv('Error', 'Mandatory fields are not set correctly, please enter a Birth Date..!!')
    #
    #     #-----Check whether enrollment has or not-------#
    #     # stu_id = super(op_student, self).create(cr, uid, vals, context=context)
    #     # enrollment_ref = self.pool.get('op.enrollment')
    #     # enrollment_count = enrollment_ref.search(cr, uid, [('student_id', '=', stu_id)], count=True, context=context)
    #     # if enrollment_count < 1:
    #     #     raise osv.except_osv(_(u'Error'), _(u'Make an Enrollment'))
    #     #     return
    #     return super(op_student, self).create(cr, uid, vals, context=context)