from openerp.osv import osv, fields, expression
import openerp.addons.decimal_precision as dp
class product_template(osv.osv):
    _inherit = "product.template"
    _columns = {
                'id_product': fields.char('Product Id :'),
                'isbn_number': fields.char('ISBN Number :'),
                'author': fields.char('Author :'),
                'publisher': fields.char('Publisher :'),
                'date_of_publish': fields.date("Date Of Publish"),
                }
class product_product(osv.osv):
    _inherit = "product.product"
    _columns = {
                'id_product': fields.char('Product Id :'),
                'isbn_number': fields.char('ISBN Number :'),
                'author': fields.char('Author :'),
                'publisher': fields.char('Publisher :'),
                'date_of_publish': fields.date("Date Of Publish"),
                }


