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


class res_partner(osv.Model):
    _inherit = 'res.partner'

    _columns = {
        'name': fields.char('Name', size=250, required=True, select=True),
        #'library_card_ids': fields.one2many('op.library.card', 'partner_id', 'Library Card', ),
        'is_student': fields.boolean('Student', readonly=True),
        #'stu_reg_id': fields.char(string='Student No.', size=7, readonly=True),
    }

    # def name_get(self, cr, uid, ids, context=None):
    #     res = []
    #     student = self.pool.get('op.student')
    #     for course in self.read(cr, uid, ids, ['name', 'responsible_id']):
    #         name = course['name'] + '(' + course['responsible_id'][1] + ')'
    #         res.append((course['id'], name))
    #     return res

    def write(self, cr, uid, ids, vals, context=None):

        stud = self.browse(cr, uid, ids, context=context)[0]

        if ('name' in vals) & (stud.is_student is True):
            raise "Cannot Edit"
        else:
            return super(res_partner, self).write(cr, uid, ids, vals, context=context)

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
