from openerp.osv import osv, fields
from openerp import api


class op_subject(osv.Model):

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

    _name = 'op.subject'
    _columns = {
        'name': fields.char(size=50, string='Name', required=True),
        'code': fields.char(size=8, string='Code', required=True),
        # 'type': fields.selection([('t', 'Theory'), ('p', 'Practical'),  ('pt','Both'), ('o', 'Other')], string='Type'),
        'type': fields.selection([('core', 'Core'), ('elective', 'Elective')], string='Type'),
        'standard_id': fields.many2one('op.standard', 'Standard', select=True, required=True),
        'rel_subjects': fields.many2one('op.student.batch.mapping', 'subject_id', select=True)
    }

    #.... check passing nul values..#
    def _check_invalid_data(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        new_name = str(obj.name)
        new_code = str(obj.code)
        name = new_name.replace(" ", "")
        code = new_code.replace(" ", "")
        n_name = ''.join([i for i in name if not i.isdigit()])
        n_code = ''.join([i for i in code if not i.isdigit()])
        #isalpha python inbuilt function Returns true if string
            #has at least 1 character and all characters are alphabetic and false otherwise.
        if name or code:
            if n_code.isalpha() or code.isdigit():
                if n_name.isalpha() or name.isdigit():
                    return True
        else:
            return False

    _constraints = [
                    (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
    ]

    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the SUBJECT must be unique!')]


