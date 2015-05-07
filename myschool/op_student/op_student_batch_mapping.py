from openerp.osv import osv, fields


class op_student_batch_mapping(osv.Model):
    _name = 'op.student.batch.mapping'

    _columns = {
        'student_id': fields.many2one('op.student', string='Student'),
        'batch_id': fields.many2one('op.batch', string='Batch', domain="[('course_id', '=', course_id)]",
                                    required=True, options="{'create_edit': False }"),
        'standard_id': fields.many2one('op.standard', string='Standard', domain="[('course_id', '=', course_id)]",
                                        required=True, options="{'create_edit': False }"),

        'subject_id': fields.many2one('op.subject', string='Subjects', domain="[('standard_id', '=', standard_id)]",
                                       required=True),


        'default_course': fields.boolean('Default Course'),
        'course_id': fields.many2one('op.course', 'Course', required=True),
        'product_id': fields.related('product_id', 'name', string='Related Product', type='char', readonly=True),
        # 'payment_term': fields.many2one('account.payment.term', 'Payment Terms'),
    }

    def create(self, cr, uid, vals, context=None):
        def_count = self.search(cr, uid,
                                ['&', ('student_id', '=', vals['student_id']), ('default_course', '=', True)],
                                context=context)
        if len(def_count) < 1:
            vals.update({'default_course': True})
        elif 'default_course' in vals:
            if vals['default_course']:
                old_def = self.browse(cr, uid, def_count, context=context)
                self.write(cr, uid, old_def[0].id, {'default_course': False}, context=context)

        return super(op_student_batch_mapping, self).create(cr, uid, vals, context=context)

    def clear_defaults(self, cr, uid, sid, context=None):
        def_count = self.search(cr, uid,
                                ['&', ('student_id', '=', sid), ('default_course', '=', True)],
                                context=context)
        if len(def_count) > 0:
            old_def = self.browse(cr, uid, def_count, context=context)
            for crs in old_def:
                self.write(cr, uid, crs.id, {'default_course': False}, context=context)

    def student_default(self, cr, uid, sid, context=None):
        def_count = self.search(cr, uid,
                                ['&', ('student_id', '=', sid), ('default_course', '=', True)],
                                context=context)
        if len(def_count) > 0:
            old_def = self.browse(cr, uid, def_count, context=context)
            return old_def[0]
        return False

    def set_default_course(self, cr, uid, sid, cid, context=None):

        def_new = self.search(cr, uid,
                              ['&', ('student_id', '=', sid), ('course_id', '=', cid)],
                              context=context)

        old_def = self.browse(cr, uid, def_new, context=context)
        if old_def:
            # self.clear_defaults(cr, uid, sid, context)
            self.write(cr, uid, old_def[0].id, {'default_course': True}, context=context)
        else:
            raise osv.except_osv(_(u'Error'), _(u'Record not found'))

        return True

    # related to the payment schedule button object
    def view_details(self, cr, uid, ids, context=None):
        res = {}
        stu_bat_map = self.pool.get('op.student.batch.mapping')
        course_ids = stu_bat_map.search(cr, uid, [('id', '=', ids)], context=context)
        stu_bat_map_obj = stu_bat_map.browse(cr, uid, course_ids, context=context)
        stu_bat_map_course_id = stu_bat_map_obj[0].course_id
        course = self.pool.get('op.course')
        course_id = course.search(cr, uid, [('id', '=',  stu_bat_map_course_id.id)], context=context)
        # product_id = course[0]
        cr.execute('SELECT product_id FROM op_course '\
                   'WHERE id=%s',(course_id))

        course_product = course.browse(cr, uid, map(lambda x: x[0], cr.fetchall()))
        product_id = course_product[0].id
        print product_id
        product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
        product_price = product.price_get('list_price')[product.id]
        print product_price
        res = [product_id, product_price]

        # product_data = ({'product_id': product_id,
        #                     'list_price': product_price})
        #
        # obj_payment = self.pool.get('op.payment.schedule')
        # payid = obj_payment.create(cr, uid, product_data, context=context )
        # obj_payment.update( payid)
        #
        # return super('op_student_batch',self).create(cr, uid, obj_payment,context=context)
        return {
            'res_model': 'op.payment.schedule',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'op.payment.schedule',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',#current
            'context': {'test': res}
                }



