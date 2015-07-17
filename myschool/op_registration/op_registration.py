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
            [('d', 'Draft'), ('i', 'Confirm'), ('s', 'Enroll'), ('done', 'Done'), ('r', 'Rejected'), ('p', 'Pending'),
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

    def confirm_in_progress(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'i'})
        return True

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

    def confirm_pending(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'p'})
        return True

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
            'view_type': 'form',
            'view_mode': 'form, tree',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view[1] or False, 'form'),
                      (tree_view and tree_view[1] or False, 'tree')],
            'type': 'ir.actions.act_window',
            # 'res_id': student.id,
            'target': 'new',
            }
        self.write(cr, uid, ids, {'state': 'done'})
        return value

op_registration()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

