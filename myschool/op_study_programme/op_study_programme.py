from openerp.osv import fields
from openerp.osv import osv
from openerp import api
from openerp.tools.translate import _


class op_study_programme(osv.Model):

    #--Code change to upper case---
    @api.onchange('code')
    def onchange_case(self, cr, uid, ids, code):
        if code != False:
            result = {'value': {
                'code': str(code).upper()
            }
            }
            return result
        else:
            return True

    _name = 'op.study.programme'
    _rec_name = 'name'
    _columns = {
        'code': fields.char('Code', required=True, size=20),
        'name': fields.char('Name', required=True, size=70),
        'res_person': fields.many2one('res.partner', 'Responsible Person'),
        'parent': fields.many2one('op.study.programme', 'Parent'),
    }

    # ----------------Validations----------------------- s#
    # ---------code validation------------- s#
    def code_validation(self, cr, uid, ids, code):
        st_code = str(code).replace(" ", "")
        st_prm_code = ''.join([i for i in st_code if not i.isdigit()])
        if str(code).isspace():
            raise osv.except_osv(_('Invalid Code !'), _('Only Spaces not allowed'))
        elif st_prm_code.isalpha() or st_code.isdigit():
            return True
        else:
            raise osv.except_osv(_('Invalid Code !'), _('Please Enter the code correctly'))

    # -----------name validation----------- s#
    def name_validation(self, cr, uid, ids, name):
        if str(name).isspace():
            raise osv.except_osv(_('Invalid Name !'), _('Only Spaces not allowed'))
        else:
            return True

    # ------------Override the create method----------- s#
    def create(self, cr, uid, vals, context=None):
        # ----------code validation caller------- s#
        if 'code' in vals:
            self.code_validation(cr, uid, [], vals['code'])

        # ----------name validation caller------- s#
        if 'name' in vals:
            self.name_validation(cr, uid, [], vals['name'])

        # --------removing white spaces---------- s#
        name = vals['name'].strip().title()
        vals.update({'name': name})

        return super(op_study_programme, self).create(cr, uid, vals, context=context)

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

        return super(op_study_programme, self).write(cr, uid, ids, values, context=context)

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Study Programme must be unique!')]