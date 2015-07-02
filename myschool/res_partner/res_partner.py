# -*- coding: utf-8 -*-
# /#############################################################################
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
from openerp.tools.translate import _
# from openerp import _
from openerp.exceptions import Warning


class res_partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
        'name': fields.char('Name', size=40, required=True, select=True),
        #'library_card_ids': fields.one2many('op.library.card', 'partner_id', 'Library Card', ),
        'is_student': fields.boolean('Student', readonly=True),
        #'stu_reg_id': fields.char(string='Student No.', size=7, readonly=True),
    }

    #.... check passing nul values..#
    def _check_invalid_data(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        new_name = str(obj.name)
        name = new_name.replace(" ", "")
        #isalpha python inbuilt function Returns true if string
            #has at least 1 character and all characters are alphabetic and false otherwise.
        if name:
            if name.isalpha():
                return True
            else:
                return False
        else:
            return False

    _constraints = [
                    (_check_invalid_data, 'Entered Invalid Data!!', ['name']),
    ]

    def create(self, cr, uid, vals, context=None):
        name = vals['name'].strip()
        vals.update({'name':name})
        return super(res_partner, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids,  values, context=None):
        if 'name' in values:
            name = values['name'].strip()
            values.update({'name': name})
        return super(res_partner, self).write(cr, uid, ids,  values, context=context)


    # def name_get(self, cr, uid, ids, context=None):
    #     res = []
    #     student = self.pool.get('op.student')
    #     for course in self.read(cr, uid, ids, ['name', 'responsible_id']):
    #         name = course['name'] + '(' + course['responsible_id'][1] + ')'
    #         res.append((course['id'], name))
    #     return res

    # def write(self, cr, uid, ids, vals, context=None):
    #
    #     stud = self.browse(cr, uid, ids, context=context)[0]
    #
    #     if ('name' in vals) & (stud.is_student is True):
    #         raise Warning(_("Cannot Edit the Student."))
    #     else:
    #         return super(res_partner, self).write(cr, uid, ids, vals, context=context)
