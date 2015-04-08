from openerp.osv import osv, fields

class op_payment_schedule(osv.Model):
    _name = 'op.payment.schedule'
    _description = 'Payment Schedule'
    # _inherits = {'account.payment.term': 'account_payment_term_id'}
    _columns = {

        'product_id': fields.many2one('product.product', 'Product Name'),
        'list_price': fields.float('Product Price'),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms'),
        'invoice_date': fields.date(string='Invoice Date'),
        'student_payment_id': fields.many2one('op.student', 'Student'),
        # 'product': fields.related('product_id', 'name', string='Batch', type='char', readonly=True),
        'schedule_lines': fields.one2many('op.payment.schedule.lines', 'payment_schedule_lines_ids', string='Lines'),
    }

    #function for obtain price according to the product id
    # def onchange_product_id(self, cr, uid, ids, product_id, context=None):
    #     res = {}
    #     if product_id:
    #         product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
    #         amount_unit = product.price_get('list_price')[product.id]
    #         res['list_price'] = amount_unit
    #     return {'value': res}

    def default_get(self, cr, uid, fields, context=None):#fields_list
        res ={}
        print fields
        test_list = context.__getitem__('test')
        print test_list[0]
        print test_list[1]


        # for line in test_list:
        #     for element in line:
        #
        #         payment_schedule = self.pool.get('op.payment.schedule')
        #         payment_ids = payment_schedule.search(cr, uid, [('id', '=', element)], context=context)
        #         payment_obj = payment_schedule.browse(cr, uid, payment_ids, context=context)
        #
        #         price = payment_obj[0].list_price
        #         payment_term_id = payment_obj[0].payment_term.id
        #         invoice_date = payment_obj[0].invoice_date
        #
        #         print price
        #         print payment_term_id
        #         print invoice_date
        #
        #         p_sch_list = self.pool.get('account.payment.term').compute(cr, uid, payment_term_id, price, date_ref=invoice_date)
        #         print p_sch_list
        #
        #         for list_tuple in p_sch_list:
        #             schedule_lines = []
        #             schedule_lines.append((0, 0, {'due_date': list_tuple[0],'amount': list_tuple[1]}))
        #         # payment_schedule.create(cr, uid, {'schedule_lines': schedule_lines}, context)
        pass

        product_id = test_list[0]
        product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
        pro_name = product.name_template
        product_price = test_list[1]
        obj_pay_sch = self.pool.get('op.payment.schedule')



        return res

    # def write(self, cr, uid, ids, values, context=None):
    #     list = self.default_get(cr, uid, ids, context)
    #     print list
    #
    #     return super(op_payment_schedule, self).write(cr, uid, ids, values, context=context)

    # def my_test(self,cr, uid, ids, context=None):
    #     pass
    #     return



class op_payment_schedule_lines(osv.Model):

    _name = 'op.payment.schedule.lines'
    _columns = {
                'payment_schedule_lines_ids': fields.many2one('op.payment.schedule', 'Payment Schedule'),
                'due_date': fields.date('Due Date'),
                'amount': fields.float('Amount'),
                'status': fields.boolean('Paid/Not'),
                }


