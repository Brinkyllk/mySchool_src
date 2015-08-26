from openerp.osv import osv, fields
import datetime
from openerp import api
import re
from openerp.tools.translate import _



class op_batch(osv.Model):

    # @api.onchange('code')
    # def onchange_case(self, cr, uid, ids, code):
    #     if code != False:
    #         result = {'value': {
    #             'code': str(code).upper()
    #         }
    #         }
    #         return result
    #     else:
    #         return True

    _name = 'op.batch'
    _columns = {
        'batch_code': fields.char(string='Code', select=True, readonly=True),
        'name': fields.char(size=25, string='Name', required=True),
        'study_prog_code': fields.many2one('op.study.programme', string="Study Programme", required=True),
        'batch_no': fields.char(size=3, string='Batch No', required=True),
        'planned_start_date': fields.date(size=15, string='Planned Start Date', required=True),
        'planned_end_date': fields.date(size=15, string='Planned End Date', required=True,),
        'actual_start_date': fields.date(size=15, string="Actual Start Date"),
        'actual_end_date': fields.date(size=15, string="Actual End Date"),
        'price': fields.float(string='Price'),
        'state': fields.selection(
            [('planned', 'Planned'), ('running', 'Running'), ('cancel', 'Cancel'), ('finished', 'finished')],
            string='State'),
    }

    _sql_constraints = [('batch_code', 'UNIQUE (batch_code)', 'The CODE of the Batch must be unique!')]

    # .... check passing nul values....#
    def batch_name_validation(self, cr, uid, ids, batch_name):
        n_name = str(batch_name).replace(",", "")
        n_name = n_name.replace(" ", "")
        n_name = ''.join([i for i in n_name if not i.isdigit()])
        if str(batch_name).isspace():
            raise osv.except_osv(_('Invalid Batch Name !'), _('Only spaces not allowed'))
        elif n_name.isalpha():
            return True
        else:
            raise osv.except_osv(_('Invalid Batch Name'), _('Please insert valid name..!'))

    # ......Batch no validation........ s#
    def batch_no_validation(self,cr, uid, ids, batch_no):
        if str(batch_no).isspace():
            raise osv.except_osv(_('Invalid Batch Number !'), _('Only spaces not allowed'))
        elif str(batch_no).isalpha():
            raise osv.except_osv(_('Invalid Batch Number !'), _('Alphabetic Characters Not Allowed..!'))
        else:
            pass

    def create(self, cr, uid, vals, context=None):

        # ----------contact batch name validation caller by s------------- #
        if 'name' in vals:
            self.batch_name_validation(cr, uid, [], vals['name'])

        # ----------contact batch no validation caller by s------------- #
        if 'batch_no' in vals:
            self.batch_no_validation(cr, uid, [], vals['batch_no'])



        #Minus values are not allowed for the price
        if 'price' in vals:
            price = vals['price']
            if price >= 0:
                pass
            else:
                raise osv.except_osv('Value Error', 'Minus values are not allowed for the Price')

        programme = self.pool.get('op.study.programme').browse(cr, uid, vals['study_prog_code'])
        batch = vals['batch_no']
        programme_code = str(programme.code)
        btch = programme_code + ' ' + batch
        vals.update({'batch_code': btch})

        res = super(op_batch, self).create(cr, uid, vals, context=context)
        return res

    def write(self, cr, uid, ids,  values, context=None):

        # ----------contact first name validation caller by s------------- #
        if 'name' in values:
            self.batch_name_validation(cr, uid, [], values['name'])

        # ----------contact batch no validation caller by s------------- #
        if 'batch_no' in values:
            self.batch_no_validation(cr, uid, [], values['batch_no'])

        #Minus values are not allowed for the price
        if 'price' in values:
            price = values['price']
            if price >= 0:
                pass
            else:
                raise osv.except_osv('Value Error', 'Minus values are not allowed for the Price')

        programme_obj = self.browse(cr, uid, ids, context=context)
        # modification of study programme
        if ('study_prog_code' in values):
            programme = self.pool.get('op.study.programme').browse(cr, uid, values['study_prog_code'])
            programme_code = programme.code
            batch_code = programme_obj.batch_no
            btch = programme_code + ' ' + batch_code
            values.update({'batch_code': btch})

        #..modification of batch number
        if ('batch_no' in values):
            batch_number = values['batch_no']
            programme_id = programme_obj.study_prog_code
            programme = self.pool.get('op.study.programme').browse(cr, uid, programme_id.id)
            programme_code = programme.code
            batch = programme_code + ' ' + batch_number
            values.update({'batch_code': batch})

        #..modification of both study programme and batch number
        if ('study_prog_code' in values) and ('batch_no' in values):
            programme = self.pool.get('op.study.programme').browse(cr, uid, values['study_prog_code'])
            programme_code = programme.code
            batch_number = values['batch_no']
            batch = programme_code + ' ' + batch_number
            values.update({'batch_code': batch})

        res = super(op_batch, self).write(cr, uid, ids,  values, context=context)
        return res


    #.... check passing nul values..#
    # def _check_invalid_data(self, cr, uid, ids, context=None):
    #     obj = self.browse(cr, uid, ids, context=context)
    #     new_name = str(obj.name)
    #     new_code = str(obj.code)
    #     new_name = re.sub('[/-]', '', new_name)
    #     name = new_name.replace(" ", "")
    #     code = new_code.replace(" ", "")
    #     n_name = ''.join([i for i in name if not i.isdigit()])
    #     n_code = ''.join([i for i in code if not i.isdigit()])
    #     #isalpha python inbuilt function Returns true if string
    #         #has at least 1 character and all characters are alphabetic and false otherwise.
    #     if name or code:
    #         if n_code.isalpha() or code.isdigit():
    #             if n_name.isalpha() or name.isdigit():
    #                 return True
    #     else:
    #         return False
    #
    # _sql_constraints = [('code', 'UNIQUE (code)', 'The CODE of the Batch must be unique!')]
    #
    def _check_date(self, cr, uid, vals, context=None):
        for obj in self.browse(cr, uid, vals):
            start_date = obj.actual_start_date
            end_date = obj.actual_end_date
            if start_date and end_date:
                datetime_format = "%Y-%m-%d"
                from_dt = datetime.datetime.strptime(start_date, datetime_format)
                to_dt = datetime.datetime.strptime(end_date, datetime_format)
                if to_dt < from_dt:
                    return False
                return True
            else:
                return True

    #Check state against start date & end date
    def _check_state(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids, context=context)
        datetime_format = "%Y-%m-%d"
        startDate = obj.planned_start_date
        fomatStartDate = datetime.datetime.strptime(startDate, datetime_format)
        endDate = obj.planned_end_date
        fomatEndDate = datetime.datetime.strptime(endDate, datetime_format)
        state = str(obj.state)
        datTime = datetime.datetime.today()
        todatDate = datTime.strftime('%Y-%m-%d')
        fomatTodayDate= datetime.datetime.strptime(todatDate, datetime_format)

        if state == 'planned':
            if fomatTodayDate < fomatStartDate < fomatEndDate:
                return True
            else:
                return False
        elif state == 'running':
            if fomatStartDate < fomatTodayDate < fomatEndDate:
                return True
            else:
                return False
        elif state == 'finished':
            if fomatStartDate < fomatEndDate < fomatTodayDate:
                return True
            else:
                return False
        else:
            return True



        #  (_check_invalid_data, 'Entered Invalid Data!!', ['name', 'code']),
    _constraints = [
        (_check_state, 'End date & Start date against State is wrong!!', ['state']),
        (_check_date, 'End Date should be greater than Start Date!', ['actual_start_date', 'actual_end_date'])
             ]
    #
    # _defaults = {
    #     'state': 'planned',
    # }
    #
    # def create(self, cr, uid, vals, context=None):
    #     code = vals['code'].strip()
    #     name = vals['name'].strip()
    #     vals.update({'code':code, 'name':name})
    #     return super(op_batch, self).create(cr, uid, vals, context=context)
    #
    # def write(self, cr, uid, ids,  values, context=None):
    #     if 'name' in values:
    #         name = values['name'].strip()
    #         values.update({'name': name})
    #     if 'code' in values:
    #         code = values['code'].strip()
    #         values.update({'code': code})
    #     return super(op_batch, self).write(cr, uid, ids,  values, context=context)