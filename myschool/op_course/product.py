from openerp.osv import osv, fields


class product_template(osv.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    _columns = {
        'iscourse': fields.boolean('Course')
    }

    def unlink(self, cr, uid, ids, context=None):
        return super(product_template).unlink(cr, uid, ids, context)

    def write(self, cr, uid, ids, vals, context=None):

        if 'name' in vals:
            rec = self.browse(cr, uid, ids, context)[0]
            if rec.iscourse:
                raise osv.except_osv('Data Integrity', 'Please edit this product from Course')

        return super(product_template, self).write(cr, uid, ids, vals, context)
