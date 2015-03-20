from osv import osv, fields


class op_classroom(osv.osv):
    _name = 'op.classroom'

    _columns = {
        'name': fields.char(size=16, string='Name', required=True),
        'code': fields.char(size=4, string='Code', required=True),
        'course_id': fields.many2one('op.course', 'Course', required=True),
        'standard_id': fields.many2one('op.standard', 'Standard', required=True),
        'capacity': fields.integer(string='No. Of Person'),
        # 'facility': fields.many2many('op.facility', 'classroom_facility_rel', 'op_classroom_id', 'op_facility_id',
        #                              string='Facilities'),
        'asset_line': fields.one2many('op.asset', 'asset_id', 'Asset', required=True),
    }


op_classroom()


class op_asset(osv.osv):
    _name = 'op.asset'

    _columns = {
        'asset_id': fields.many2one('op.classroom', 'Asset'),
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'code': fields.char('Code', size=256),
        'product_uom_qty': fields.float('Quantity', required=True),

    }
