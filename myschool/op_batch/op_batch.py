from openerp.osv import osv, fields
import datetime
from openerp import api
import re



class op_batch(osv.Model):

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

    _name = 'op.batch'
    _columns = {
        'name': fields.char(size=25, string='Name', required=True),
        'code': fields.char(size=8, string='Code', required=True),
        'start_date': fields.date(size=15, string='Start Date', required=True),
        'end_date': fields.date(size=15, string='End Date', required=True,),
        'state': fields.selection(
            [('planned', 'Planned'), ('running', 'Running'), ('cancel', 'Cancel'), ('finished', 'finished')],
            string='State'),
        'course_id': fields.many2one('op.course', string='Course', ondelete='restrict', required=True),
    }

    #.... check passing nul values..#
    def _check_invalid_data(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        new_name = str(obj.name)
        new_code = str(obj.code)
        new_name = re.sub('[/-]', '', new_name)
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




    _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Batch must be unique!')]

    def _check_date(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            start_date = obj.start_date
            end_date = obj.end_date
            if start_date and end_date:
                datetime_format = "%Y-%m-%d"
                from_dt = datetime.datetime.strptime(start_date, datetime_format)
                to_dt = datetime.datetime.strptime(end_date, datetime_format)
                if to_dt < from_dt:
                    return False
                return True

    #Check state against start date & end date
    def _check_state(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        datetime_format = "%Y-%m-%d"
        startDate = obj.start_date
        fomatStartDate = datetime.datetime.strptime(startDate, datetime_format)
        endDate = obj.end_date
        fomatEndDate = datetime.datetime.strptime(endDate, datetime_format)
        state = str(obj.state)
        datTime = datetime.datetime.today()
        todatDate = datTime.strftime('%Y-%m-%d')
        fomatTodayDate= datetime.datetime.strptime(todatDate, datetime_format)
        if state == 'planned':
            if fomatTodayDate < fomatStartDate:
                return True
            else:
                return False
        elif state == 'running':
            if fomatStartDate < fomatTodayDate:
                return True
            else:
                return False
        elif state == 'finished':
            if fomatEndDate < fomatTodayDate:
                return True
            else:
                return False
        else:
            return True

    _constraints = [
        (_check_date, 'End Date should be greater than Start Date!', ['start_date', 'end_date']),
        (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
        (_check_state, 'End date & Start date against State is wrong!!', ['state']),
    ]

    _defaults = {
        'state': 'planned',
    }

    def create(self, cr, uid, vals, context=None):
        code = vals['code'].strip()
        name = vals['name'].strip()
        vals.update({'code':code, 'name':name})
        return super(op_batch, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids,  values, context=None):
        if 'name' in values:
            name = values['name'].strip()
            values.update({'name': name})
        if 'code' in values:
            code = values['code'].strip()
            values.update({'code': code})
        return super(op_batch, self).write(cr, uid, ids,  values, context=context)